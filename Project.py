import os
import json

op1 = input("Enter \"login\" or \"register\" or \"end\": ")
while op1 != "login" and op1 != "register" and op1 != "end":
    print("Error.")
    op1 = input("Enter \"login\" or \"register\" or \"end\": ")

if os.path.exists("./users.txt"):
    with open("./users.txt", "r") as f:
        users = json.load(f)
        userCount = len(users)
else:
    with open("./users.txt", "x") as f:
        users = []
        userCount = 0

if os.path.exists("./jobs.txt"):
    with open("./jobs.txt", "r") as f:
        jobs = json.load(f)
        jobCount = len(jobs)
else:
    with open("./jobs.txt", "x") as f:
        f.close()
        jobs = []
        jobCount = 0

if os.path.exists("./proposals.txt"):
    with open("./proposals.txt", "r") as f:
        proposals = json.load(f)
        proposalCount = len(proposals)
else:
    with open("./proposals.txt", "x") as f:
        f.close()
        proposals = []
        proposalCount = 0

def findID(u):
    for i in users:
        if i[1] == u:
            return i[0]


while op1 != "end":
    if op1 == "register":
        user = input("Enter Username: ")
        pwd = input("Enter Password: ")
        confpwd = input("Confirm Password: ")
        stat = input("Enter Status (freelancer or client): ")
        while stat != "freelancer" and stat != "client":
            stat = input("Enter Status (freelancer or client): ")
        equal = False
        if confpwd == pwd:
            equal = True

        if equal:
            founduser = False
            for i in users:
                if i[1] == user and len(user) != 0:
                    founduser = True
            if founduser:
                print("User already exists.")
            else:
                if stat == "client":
                    users.append([userCount + 1, user, pwd, stat])
                    userCount += 1
                elif stat == "freelancer":
                    phone = int(input("Enter Phone number: "))
                    natID = int(input("Enter National ID: "))
                    users.append([userCount + 1, user, pwd, stat, phone, natID])
                    userCount += 1
                print("Registered Successfully.")
        else:
            print("Passwords not equal.")

    if op1 == "login":
        user = input("Enter Username: ")
        pwd = input("Enter Password: ")
        stat = input("Enter Status(freelancer or client): ")
        while stat != "freelancer" and stat != "client":
            stat = input("Enter Status (freelancer or client): ")

        found = False
        for i in users:
            if i[1] == user and i[2] == pwd and i[3] == stat:
                found = True
                print("Authentication Successful!")
                print("You are a ", stat)

        if not found:
            print("Authentication Failed, Try again.")
        else:
            if stat == "client":
                op2 = input("Enter \"add job\" or \"remove job\" or \"list freelancers\" or \"list my proposals\" or \"end\": ")

                while op2 != "end":
                    if op2 == "add job":
                        title = input("Enter Job Title: ")
                        desc = input("Enter Job Description: ")
                        skills = []
                        skillCount = 0
                        print("Enter skills, when done, enter \"0\".")
                        print("Skill ", skillCount + 1, ":-")
                        newSkill = input("")
                        while newSkill != "0":
                            skills.append(newSkill)
                            skillCount += 1
                            print("Skill ", skillCount + 1, ":-")
                            newSkill = input("")
                        if skillCount == 0:
                            skills = ["No Skills Needed."]

                        jobs.append([jobCount + 1, title, desc, skills, findID(user)])
                        jobCount += 1
                        print(title, "added successfully.")
                        print("Job ID is ", jobCount, ".")
                    elif op2 == "remove job":
                        jobid = int(input("Enter Job ID: "))
                        n = 0
                        jobFound = False
                        mine = False
                        for i in jobs:
                            if i[0] == jobid:
                                jobFound = True
                                if i[4] == findID(user):
                                    jobs.pop(n)
                                    jobCount -= 1
                                    print("Job Removed.")
                                    mine = True
                                    break
                            n += 1
                        if not mine:
                            print("Cannot remove other clients' jobs")
                        elif not jobFound:
                            print("No job found with this ID.")
                    elif op2 == "list freelancers":
                        found = False
                        for i in users:
                            if i[3] == "freelancer":
                                found = True
                                props = []
                                for j in proposals:
                                    if j[1] == i[0]:
                                        props.append(j[2])
                                print("Freelancer ID: ", i[0])
                                print("Username: ", i[1])
                                print("Phone Number: ", i[3])
                                print("National ID: ", i[4])
                                if len(props) == 0:
                                    print("Freelancer sent no proposals.")
                                else:
                                    print(i[1], "has Proposals:-")
                                    n = 0
                                    for j in props:
                                        print(n + 1, ": Job", j)
                                        n += 1
                                print("")
                            if not found:
                                print("No freelancers Found.")
                    elif op2 == "list my proposals":
                        myjobs = []
                        for i in jobs:
                            if i[4] == findID(user):
                                myjobs.append(i[0])
                        if len(myjobs) == 0:
                            print("You haven't added a job.")
                        else:
                            found = False
                            for i in myjobs:
                                for j in proposals:
                                    if j[2] == i and j[4] == "Not seen yet.":
                                        found = True
                                        print("Freelancer", j[1], "has proposed for job", j[2])
                                        if not len(j[3]) == 0:
                                            print("Freelancer has the following skills:-")
                                            n = 0
                                            for k in j[3]:
                                                print("\t", n + 1, ":", k)
                                            print("")
                            if not found:
                                print("No proposals for any of your jobs found.")
                            else:
                                op3 = ""
                                while op3 != "end" and op3 != "accept" and op3 != "reject":
                                    op3 = input("Enter \"accept\" or \"reject\" or \"end\": ")
                                if op3 == "accept":
                                    jobid = int(input("Enter Job ID: "))
                                    freeid = int(input("Enter Freelancer ID: "))

                                    for i in proposals:
                                        if i[1] == freeid and i[2] == jobid:
                                            i[4] = "Accepted"
                                    print("Proposal Accepted")
                                elif op3 == "reject":
                                    jobid = int(input("Enter Job ID: "))
                                    freeid = int(input("Enter Freelancer ID: "))

                                    for i in proposals:
                                        if i[1] == freeid and i[2] == jobid:
                                            i[4] = "Rejected"
                                    print("Proposal Rejected")

                    op2 = input("Enter \"add job\" or \"remove job\" or \"list freelancers\" or \"list my proposals\" or \"end\": ")

            elif stat == "freelancer":
                for i in jobs:
                    print("Job ID: ", i[0])
                    print("Job Title: ", i[1], "\n")
                    print("Job Description:-\n", i[2], "\n")
                    n = 0
                    print("Skills Needed:-")

                    for j in i[3]:
                        if j == "No Skills Needed.":
                            print(j)
                        else:
                            print(n + 1, ": ", j)
                            n += 1
                    print("\n\n")
                op2 = input("Enter \"search\" or \"send proposal\" or \"list my proposals\" or \"end\": ")

                while op2 != "end":
                    if op2 == "search":
                        title = input("Enter Job Title: ")
                        found = False
                        for i in jobs:
                            if i[1] == title:
                                found = True
                                print("Job ID: ", i[0])
                                print("Job Title: ", i[1], "\n")
                                print("Job Description:-\n", i[2], "\n")
                                n = 0
                                print("Skills Needed:-")

                                for j in i[3]:
                                    if j == "No Skills Needed.":
                                        print(j)
                                    else:
                                        print(n + 1, ": ", j)
                                        n += 1
                        if not found:
                            print("No job has this title.")

                    elif op2 == "send proposal":
                        jobid = int(input("Enter job ID: "))
                        found = False
                        for i in jobs:
                            if i[0] == jobid:
                                found = True
                        if not found:
                            print("No job found with that ID.")
                        else:
                            acceptance = "Not seen yet."
                            skills = []
                            skillCount = 0
                            print("Enter your skills, when done, enter \"0\".")
                            print("Skill ", skillCount + 1, ":-")
                            newSkill = input("")
                            while newSkill != "0":
                                skills.append(newSkill)
                                skillCount += 1
                                print("Skill ", skillCount + 1, ":-")
                                newSkill = input("")
                            proposals.append([proposalCount + 1, findID(user), jobid, skills, acceptance])
                            proposalCount += 1
                            print("Proposal Sent")

                    elif op2 == "list my proposals":
                        found = False
                        for i in proposals:
                            if i[1] == findID(user):
                                found = True
                                print("Job ID:", i[2])
                                print("Status:", i[4])
                                print("\n")
                        if not found:
                            print("You sent no proposals.")

                    op2 = input("Enter \"search\" or \"send proposal\" or \"list my proposals\" or \"end\": ")

    op1 = input("Enter \"login\" or \"register\" or \"end\": ")
with open("./users.txt", "w") as f:
    json.dump(users, f)
with open("./jobs.txt", "w") as f:
    json.dump(jobs, f)
with open("./proposals.txt", "w") as f:
    json.dump(proposals, f)

