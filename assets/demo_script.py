import time
import random
import grapheme
import pyautogui as pa

demo_script = """\
$ delay 200

@ 1000

< # Hello, world!
@ 200
< # This is a demonstration of cookiecutter-nim-cli
@ 2000

< # We will use the fantastic cookiecutter project by @audreyr,
< # You can get it at https://github.com/audreyr/cookiecutter
<
< # Create a project folder with example command and tests ready to tinker.
<
< cd /tmp
< cookiecutter gh:hiway/cookiecutter-nim-cli
@ 10000

< Jane Doe
@ 300
< jane@doemail.com
@ 200
< janedoe
@ 100
< Hello
@ 50
<
@ 100
<
@ 50
<
@ 100
<
@ 500

< cd hello
@ 200
< tree -C
@ 3000
$ ctrl L

< # Glance at the source code...
< pygmentize src/hello.nim
@ 5000
$ ctrl L

< # Here is the .nimble file...
< pygmentize -l nim hello.nimble
@ 5000
$ ctrl L

< # Let us build this project.
< nimble build
@ 3000
< ./bin/hello
@ 1000
< ./bin/hello --name=Audience
@ 3000
< # Nice!
@ 500
$ ctrl L

< # Here are unit tests...
< pygmentize tests/tester.nim
@ 5000
$ ctrl L

< # Let us run the tests
< nimble test
@ 5000
< # Sweet.
@ 2000
$ ctrl L

< # Give it a try :)
@ 5000
$ ctrl L
"""


class Kind(object):
    INPUT = "INPUT"
    ACTION = "ACTION"
    WAIT = "WAIT"

class Statement(object):
    kind = ""
    body = ""

    def __repr__(self):
        return f"{self.kind}: {self.body}"

    def validate(self):
        raise NotImplementedError()


class InputStatement(Statement):
    def __init__(self, body):
        self.kind = Kind.INPUT
        self.body = self.validate(body)

    def validate(self, body):
        body = body.strip()
        return body

    def render_keys(self):
        need_more = False
        previous = ""
        if self.body.strip().startswith("#"):
            pa.typewrite(self.body, interval=0.005)
        else:
            for gr in grapheme.graphemes(self.body):
                if need_more and previous == "^":
                    pa.keyDown('ctrl')
                    pa.press(gr)
                    pa.keyUp('ctrl')
                    need_more = False
                    previous = ""
                    continue
                if gr in ["^"]:
                    need_more = True
                    previous = gr
                    continue
                pa.press(gr)
                time.sleep(random.choice(range(1, 50)) / 1000.0)
        if not self.body.strip().endswith("<<"):
            pa.press("enter")


class ActionStatement(Statement):
    def __init__(self, body):
        self.kind = Kind.ACTION
        self.body = self.validate(body)

    def validate(self, body):
        body = body.strip()
        return body

    @property
    def action(self):
        return self.body.strip().lower()


class WaitStatement(Statement):
    def __init__(self, body):
        self.kind = Kind.WAIT
        self.body = self.validate(body)

    def validate(self, body):
        body = body.strip()
        if body == "<<":
            return body
        try:
            return int(body)
        except TypeError as e:
            e.args = e.args + f("Expected '<<' or delay in milliseconds. Got: {body}",)
            raise e

    @property
    def delay(self):
        try:
            return int(self.body) / 1000.0
        except ValueError:
            return 0

    @property
    def input(self):
        return self.body == "<<"




def parse_kind(line):
    ln = line.strip()
    if ln.startswith("<"):
        return Kind.INPUT
    elif ln.startswith("$"):
        return Kind.ACTION
    elif ln.startswith("@"):
        return Kind.WAIT


def parse_body(line):
    return line.strip()[1:].strip()


def parse_line(line):
    kind = parse_kind(line)
    body = parse_body(line)
    if kind == Kind.INPUT:
        cls = InputStatement
    elif kind == Kind.ACTION:
        cls = ActionStatement
    elif kind == Kind.WAIT:
        cls = WaitStatement
    else:
        return
    stm = cls(body)
    return stm


def parse_script(script):
    for line in script.split('\n'):
        yield parse_line(line)


def render_statement(statement):
    stm = statement
    if not stm:
        print("")
        return None, None
    print(stm)
    if stm.kind == Kind.WAIT:
        if stm.delay:
            time.sleep(stm.delay)
        else:
            input("Press ENTER to continue...")
    elif stm.kind == Kind.ACTION:
        toggles = ["ctrl", "alt", "meta", "shift"]
        if stm.action == "beep":
            print("\a")
        elif stm.action.startswith("delay"):
            delay = int(stm.action.replace("delay", ""))
            print("SET DEFAULT DELAY", delay)
            return "delay", delay
        elif not any([x in toggles for x in stm.action.split()]):
            raise ValueError(f"Unexpected action: {stm.action!r}")
        if "ctrl" in stm.action:
            pa.keyDown('ctrl')
        if "shift" in stm.action:
            pa.keyDown('shift')
        if "alt" in stm.action or "meta" in stm.action:
            print("Alt")
            pa.keyDown('alt')
        if "tab" in stm.action:
            pa.keyDown("tab")
            pa.keyUp("tab")
        else:
            chars = stm.action.replace("ctrl", "").replace("shift", "").replace("meta", "").replace("shift", "").strip()
            print(f"{chars!r}")
            pa.typewrite(chars)
        if "ctrl" in stm.action:
            pa.keyUp('ctrl')
        if "shift" in stm.action:
            pa.keyUp('shift')
        if "alt" in stm.action or "meta" in stm.action:
            pa.keyUp('alt')
    elif stm.kind == Kind.INPUT:
        stm.render_keys()
    else:
        raise ValueError(f"Unexpected statement: ", type(stm).__name__)
    return None, None


def render_script(script):
    delay = 50
    for stm in parse_script(script):
        action, body = render_statement(stm)
        if action == "delay":
            delay = body
        time.sleep(delay/1000.0)


render_script(demo_script)
