from brownie import accounts, D21


def deploy_D21():
    owner = accounts[0]
    account = accounts[0]
    contract = D21.deploy({"from":account})
    return contract

def deploy_D21_with_subjects():
    owner = accounts[0]
    d21 = D21.deploy({'from': owner})

    #Add subjects to the deployment
    subjects = ['Party of Freedom', 'Communist Party', 'Republican Party', 'Democratic Party']
    
    for i in range(len(subjects)):
        d21.addSubject(subjects[i],{"from":accounts[i]})

    return d21

def main():
    deploy_D21()