# contingency_k
Advanced Key Logger With Persistency on Windows System

1. What is this?
   - Keylogger
   - Sends logged data by email(anonymous mail is recommended)
   - Data is encoded to make it not readable(use decod.py)
   - Persistency
   - Delete trace
   - Acquire target's info
     
2. How did this acquire persistency
   - Achive UAC with secret method(read the code)
   - Set windows registry to run everytime on startup
     
3. Which trace is being removed
   - Traces in windows registry is removed
   - History of programs that executed are being erased
     
4. Which info is acquired
   - Basic system info
   - Installed program
   - Rescent doc
   - Rescent path
     
5. How to exe it
   - Use different method to create exe file with pld.spec, startups.spec
     
6. Why 2 exe program is needed?
   - It helps to avoid AV
     
8. How to use it
   - Get physical access to victim's pc
   - Execute startups.exe
   - Done
   - On every startup the program will startup automatically and get admin access without prompt(UAC) WOW!
   - Now wait for the email to come
   - If you want to erease exe and other trace from victim's pc, type special command to email

9. Ways to improve this thing
    - Method to achive persistency and admin access on every start in this code is very strong
    - Using this method you can achive any kind of presistent malicious program
    - However you need admin access on first run for now
      
11. Disclaimer
    - I am not responsible for anyone who use this code and makes problem
