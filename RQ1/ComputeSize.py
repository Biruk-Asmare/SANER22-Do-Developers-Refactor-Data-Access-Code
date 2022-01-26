import pandas as pd
import subprocess
import json
import threading

REPO_NAMES=["bio2rdf_bio2rdf-scripts","eclipse-ee4j_eclipselink","adempiere_adempiere","appirio-tech_direct-app","dotCMS_core","wso2_carbon-apimgt","oltpbenchmark_oltpbench","mtotschnig_MyExpenses","querydsl_querydsl","wordpress-mobile_WordPress-Android","AppLozic_Applozic-Android-SDK","xipki_xipki","deegree_deegree3","mirakel-android","k9mail-k-9"]
REPO_NAME_ALIASS=["","eclipselink","adempiere","direct-app","dotCMS-core","carbon-apimgt","oltpbench","MyExpenses","querydsl","WordPress-Android","Applozic-Android-SDK","xipki","deegree-3","",""]
REPO_PATH="/home/biruk/Documents/repos"
def compute_code_size(row, total):
    try:
        repo=row.repo
        ind= REPO_NAME_ALIASS.index(repo)
        repo=REPO_NAMES[ind]
        sha=row.sha
        file_name=row.file_name
        try:
            #2: compute the code size
            cmd="cloc {} --quiet --json".format(file_name).split()
            result=subprocess.run(cmd, cwd='{}/{}'.format(REPO_PATH,repo),stdout=subprocess.PIPE)
            res=result.stdout.decode('ascii').strip()
            res=json.loads(res)
            print("*** finishd {}/{}".format(row.name,total))
            return res["Java"]["code"]
        except Exception as e:
             #1 checkout to the given commit
            cmd="git checkout {}".format(sha).split()
            result=subprocess.run(cmd, cwd='{}/{}'.format(REPO_PATH,repo),stdout=subprocess.PIPE)
            #2: compute the code size
            cmd="cloc {} --quiet --json".format(file_name).split()
            result=subprocess.run(cmd, cwd='{}/{}'.format(REPO_PATH,repo),stdout=subprocess.PIPE)
            res=result.stdout.decode('ascii').strip()
            res=json.loads(res)
            #3 GO BACK TO HEAD
            cmd="git checkout {}".format('HEAD').split()
            result=subprocess.run(cmd, cwd='{}/{}'.format(REPO_PATH,repo),stdout=subprocess.PIPE)
            print("*** finishd {}/{}".format(row.name,total))
            return res["Java"]["code"]

    except Exception as e:
        print("*****************************")
        print(str(e))
        print("*****************************")
        print("*** finishd with {} {}/{}".format(-1,row.name,total))
        return -1

def main():
    exp=pd.read_csv("RQ1-exploded-data.csv")
    dsmall=exp.drop_duplicates(subset=["repo","sha","file_name"], keep="last")
    #remove this later
    dsmall=dsmall[dsmall["repo"]=="xipki"]

    #finish remove
    total=len(dsmall.index)
    print(total)
    dsmall["code_size"]=dsmall.apply(compute_code_size,axis=1,args=(total,))
    dsmall.to_csv("RQ1-xipki-exploded-data-unique-subset-with-size.csv", index=False)
    #next you merge the big dataset with this

main()
