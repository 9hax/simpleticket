# notes on implementing different features in the future

## password hashing 


>>> bcrypt.hashpw("1234".encode("utf-8"), bcrypt.gensalt(12)) 
b'$2b$12$qn5/smdnX.anrihF/k2gReIeHCdHp2QGMVX3lLPm9c0AVPSL4YzXS'
>>> bcrypt.checkpw("1234".encode("utf-8"), b'$2b$12$qn5/smdnX.anrihF/k2gReIeHCdHp2QGMVX3lLPm9c0AVPSL4YzXS')
True
>>> bcrypt.checkpw("1236".encode("utf-8"), b'$2b$12$qn5/smdnX.anrihF/k2gReIeHCdHp2QGMVX3lLPm9c0AVPSL4YzXS')
False