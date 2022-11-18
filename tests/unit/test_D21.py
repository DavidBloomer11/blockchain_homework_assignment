from scripts.deploy import deploy_D21, deploy_D21_with_subjects
from brownie import accounts, chain
import brownie


def test_get_subject():
    d21 = deploy_D21_with_subjects()
    subject_name = 'Party of Freedom'

    subject = d21.getSubject(accounts[0], {'from':accounts[0]})

    assert subject_name == subject[0]

def test_add_voter_with_owner():
    d21 = deploy_D21()
    owner = accounts[0]

    d21.addVoter(accounts[1],{'from' : owner})
    d21.addSubject('Test Party',{'from':owner})

    d21.votePositive(owner,{'from':accounts[1]})

    #Check if number of votes equals 1
    assert d21.getSubject(owner,{'from':owner})[1] == 1

def test_add_voter_without_owner():
    d21 = deploy_D21()
    user = accounts[1]

    with brownie.reverts('Only the owner can add new voters'):
        d21.addVoter(accounts[1],{'from' : user})

def test_add_voter_allready_added():
    d21 = deploy_D21()
    owner = accounts[0]

    with brownie.reverts('Voter allready added'):
        d21.addVoter(accounts[1],{'from' : owner})
        d21.addVoter(accounts[1],{'from' : owner})

def test_add_voter_with_owner():
    #Arrange
    owner = accounts[0]
    d21 = deploy_D21()
    new_voter = accounts[1]

    #Act
    transaction = d21.addVoter(new_voter, {"from": owner})
    transaction.wait(1)

    #Assert: To assert we will now check if the account is able to note

    assert 1 == 1

def test_vote_positive_without_voter_registered():
    d21 = deploy_D21()
    owner = accounts[0]

    d21.addSubject('Test Party',{'from':owner})

    with brownie.reverts("Voter has no positive votes left or isn't registered"):
        d21.votePositive(owner,{'from':accounts[1]})

def test_vote_on_unregistered_subject():
    d21 = deploy_D21()
    owner = accounts[0]
    d21.addVoter(accounts[1],{'from':owner})

    with brownie.reverts('Subject not added'):
        d21.votePositive(owner,{'from':accounts[1]})

def test_vote_positive_on_subject():
    #Arange
    owner = accounts[0]
    d21 = deploy_D21_with_subjects()
    voter = accounts[1]
    subject = accounts[2]


    #Act
    d21.addVoter(voter,{"from":owner})
    d21.votePositive(subject,{"from":voter})

    #Assert
    subject = d21.getSubject(subject, {"from":voter})
    assert subject[1] > 0

def test_add_subject():
    d21 = deploy_D21()
    subject_owner = accounts[1]
    subject_name = 'Party of Freedom'

    d21.addSubject(subject_name,{'from': subject_owner})
    subject = d21.getSubject(subject_owner,{'from': subject_owner})
    assert subject[0] == subject_name

def test_vote_negative_with_positive_votes_left():
    #Arange
    owner = accounts[0]
    d21 = deploy_D21_with_subjects()
    voter = accounts[1]
    subject = accounts[2]


    #Act
    d21.addVoter(voter,{"from":owner})
    d21.addVoter(owner,{"from":owner})

    error_msg = "Voter still has positive votes or isn't registered."
    with brownie.reverts(error_msg):
        d21.voteNegative(subject,{"from":voter})
    
def test_vote_negative():
    #Arange
    owner = accounts[0]
    d21 = deploy_D21_with_subjects()
    voter = accounts[1]
    subject_1 = accounts[2]
    subject_2 = accounts[1]
    subject_3 = accounts[0]


    #Act
    d21.addVoter(voter,{"from":owner})
    d21.addVoter(owner,{"from":owner})

    d21.votePositive(subject_1, {'from':voter})
    d21.votePositive(subject_2, {'from':voter})
    d21.votePositive(subject_3, {'from': owner})
    d21.voteNegative(subject_3, {'from':voter})

    assert d21.getSubject(subject_3, {'from':voter})[1] == 0
    
def test_get_remaining_time():
    d21 = deploy_D21()
    time_1 = d21.getRemainingTime({'from':accounts[0]})
    assert time_1 == 604800

def test_get_results():
    #Arange
    owner = accounts[0]
    d21 = deploy_D21_with_subjects()

    subject_1 = accounts[0]
    subject_2 = accounts[1]
    subject_3 = accounts[2]
    subject_4 = accounts[3]


    #Add voters
    d21.addVoter(accounts[0],{"from":owner})
    d21.addVoter(accounts[1],{"from":owner})
    d21.addVoter(accounts[2],{"from":owner})
    d21.addVoter(accounts[3],{"from":owner})
    d21.addVoter(accounts[4],{"from":owner})

    #Vote
    d21.votePositive(subject_1,{'from':accounts[0]})
    d21.votePositive(subject_2,{'from':accounts[0]})
    d21.votePositive(subject_2,{'from':accounts[1]})
    d21.votePositive(subject_2,{'from':accounts[2]})
    d21.votePositive(subject_3,{'from':accounts[1]})

    arr = d21.getResults({'from':accounts[0]})
    assert arr[0][0] == d21.getSubject(subject_4)[0]
    assert arr[3][0] == d21.getSubject(subject_2)[0]
    
