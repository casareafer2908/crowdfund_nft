from scripts.mint_oneTM_nft import mint2


def deploy10():
    toDeploy = 1
    for n in range(toDeploy):
        print(f"run number {(n + 1)}")
        mint2()


def main():
    deploy10()
