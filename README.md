# Cloud Security Auditor: Project Overview
I built this tool to solve a specific problem: it’s way too easy for cloud accounts to end up with "identity bloat" where everyone has too much power. This script automates the process of finding those risks so I don't have to hunt for them manually.

### What it actually does
The script connects to my AWS account and pulls a full list of IAM users. It then iterates through every single user and group to see if they are carrying the AdministratorAccess policy. If it finds someone with "God Mode" enabled, it flags them as a critical risk.

### The technical flow
The Scan: It uses Python and Boto3 to talk to the IAM service.

The Output: It generates two files—a JSON file for data analysis and a text file for a quick human-readable summary.

The Vault: It uploads those reports to a private S3 bucket.

### Why I bothered with the extra security
I didn't want my security reports just sitting in an open folder. I added a couple of layers to make sure the audit itself is as secure as the account I'm scanning.

Encryption: I used AES-256 server-side encryption. This means that if someone somehow got access to the physical storage, the data would be unreadable gibberish.

Object Lock: I enabled a 7-day governance lock. This ensures that even if I accidentally tried to delete my logs (or if a hacker tried to hide their tracks), the files are undeletable until the timer runs out.

Versioning: The bucket keeps track of every version of every audit, giving me a full timeline of when permissions changed.

### Lessons learned
Setting this up taught me that cloud security isn't just about clicking buttons in a console. It's about building a pipeline that respects the Principle of Least Privilege. By writing this in Python, I can now audit an account with 1,000 users just as quickly as I can audit one with two users.
