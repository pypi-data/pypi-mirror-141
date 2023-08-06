import logging
import os
from subprocess import run
from shutil import rmtree

from requests import post

from ocs.args import args
from ocs.data import contest_data, problem_data
from ocs.db import con, cur
from ocs.languages import languages


def process(username, homeserver, token, contest, problem, language, code):
    """Process a submission"""

    number = int(cur.execute('SELECT Count(*) FROM "' + contest + '_submissions"').fetchone()[0])
    cur.execute('INSERT INTO "' + contest + '_submissions" VALUES (?, ?, ?, ?, ?, ?)',
                (number, username, homeserver, problem, code, 0))

    if language not in languages:
        return 400  # Bad request

    if '@' not in problem:  # Local
        verdict = run_local(contest, problem, language, code, number)
        rmtree(os.path.join('/tmp',  contest, str(number)))  # Clean up
    else:  # Remote
        verdict = run_remote(username, homeserver, token, problem, language, code, number)

    logging.info(verdict)

    # Update submissions table
    cur.execute('UPDATE "' + contest + '_submissions" SET verdict = ? WHERE number = ?', (verdict, number))

    # Update status table
    if cur.execute('SELECT Count(*) FROM "' + contest + '_status" WHERE username = ? AND homeserver = ?',
        (username, homeserver)).fetchone()[0] == 0:
        cur.execute('INSERT INTO "' + contest + '_status" VALUES ("' + username + '", "' + homeserver +
                    '"' + ', 0' * len(contest_data[contest]['problems']) + ')')
    cur.execute('UPDATE "' + contest + '_status" SET "' + problem +
                '" = ? WHERE username = ? AND homeserver = ?', (str(verdict), username, homeserver))
    
    con.commit()

    return verdict


def run_local(contest, problem, language, code, number):
    """Run a program locally"""

    # Save the program
    tmpdir = os.path.join('/tmp', contest, str(number))
    os.makedirs(tmpdir, exist_ok=True)
    with open(os.path.join(tmpdir, 'main.' + language), 'w') as f:
        f.write(code)

    # Compile the code if needed
    if not languages[language].compile is None:
        ret = run('timeout 10 ' + languages[language].compile,
                  shell=True, cwd=tmpdir)
        if ret:
            return 500

    tcdir = os.path.join(args.contests_dir, contest, problem)
    problem_info = problem_data[contest][problem]
    time_limit = problem_info['time-limit']
    memory_limit = problem_info['memory-limit']
    check = problem_info['checker'] if 'checker' in problem_info else 'diff -Bw'

    tc = 1
    while os.path.isfile(os.path.join(tcdir, str(tc) + '.in')):
        # Run test case
        ret = run('firejail --noprofile --net=none --whitelist={} --rlimit-cpu={} --rlimit-as={}k {} < {} > out'.format(tcdir, time_limit,
                  memory_limit, languages[language].run, os.path.join(tcdir, str(tc) + '.in')), shell=True, cwd=tmpdir).returncode
        if not ret == 0:
            return 408  # Runtime error

        # Run checker on output
        ret = run(check + ' ' + os.path.join(tmpdir, 'out') + ' ' + os.path.join(tcdir, str(tc) + '.out'), shell=True).returncode
        os.remove(os.path.join(tmpdir, 'out'))  # Delete output
        if not ret == 0:
            return 406  # Wrong answer
        tc += 1

    return 202  # All correct!


def run_remote(username, homeserver, token, problem, language, code, number):
    """Run a program remotely"""

    problem, contest, server = problem.split()
    return post(('https://' if server.find('://') == -1 else '') + server, json={'type': 'submit', 'username': username,
        'homeserver': homeserver, 'token': token, 'contest': contest, 'problem': problem, 'code': code, 'number': number
    }).statuscode
