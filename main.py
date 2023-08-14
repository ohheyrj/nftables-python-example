from client import Nftables

nft_client = Nftables(9000, 'testing_comment')
nft_client.delete_rule()