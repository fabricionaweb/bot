import os, re

class CodeValidator():
    warn_statements = [r"\bprompt\b", "\balert\b", r"\bconfirm\b", r"document\.write"]
    valid_extensions = [".css", ".js", ".map",
        ".png", ".jpg", ".jpeg", ".gif", ".ico",
        ".otf", ".eot", ".svg", ".ttf", ".woff"]

    def validate_code(self, files):
        issues = []

        for file in files:
            if file["extension"] not in self.valid_extensions:
                issues.append("*{extension}* (on *{name}*) seems odd to want to host?".format(**file))
                continue

            if not (file["extension"] == ".js" or file["extension"] == ".css"):
                continue
            
            if re.search(r"\bmin\b", file["name"]):
                #warn if more than 10 lines in "minimized" file
                if len(file["contents"].splitlines(True)) > 10:
                    issues.append("Is {name} ({version}) properly minimized?".format(**file))

            for test in self.warn_statements:
                if re.search(test, file["contents"]):
                    issues.append("Expression `{0}` had a match in the contents of *{name}* ({version}).".format(test, **file))

            #no comments... could be more sound by checking start
            # if not re.search(r"(?:\/\*(?:[\s\S]*?)\*\/)|(?:([\s;])+\/\/(?:.*)$)", file["contents"], re.MULTILINE):
            #     issues.append("*{name}* ({version}) probably should start with a header detailing author and code source".format(**file))

        return issues
