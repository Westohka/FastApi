from passlib.context import CryptContext

pwd_cxt = CryptContext( schemes = ["bcrypt"], deprecated = "auto" )

class Hash:
    @classmethod
    def crypt( cls, data ):
        return pwd_cxt.hash( data )

    @classmethod
    def verify( cls, hashed_data, plain_data ):
        return pwd_cxt.verify( plain_data, hashed_data )
