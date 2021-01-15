import os
import subprocess


my_env = os.environ.copy()
my_env["PUBLIC_URL"] = (
    "https://andrew-chen-wang.github.io/spa-with-sessions-static"
)
output = subprocess.check_output(
    "cd my-app && npm run build",
    env=my_env,
    shell=True
)
print(output)
