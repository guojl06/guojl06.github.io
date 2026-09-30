#pragma once
# include "User.h"
# include "EncryptStrategy.h"
# include "VerificationStrategy.h"


class UserProxy{
    // friend class RealUser;
    RealUser *ruser;
    EncryptStrategy *encStr;
    VerificationStrategy *verStr;
    public:
    UserProxy(RealUser *ru,EncryptStrategy *en,VerificationStrategy *ve):
        ruser(ru),encStr(en),verStr(ve){};

    void sendMessage(std::string mes){
        
        ruser->sendMessage(encStr->encode(mes));
        // std::cout << encStr->encode(mes) << std::endl;
        std::cout << verStr->verify(mes) << std::endl;
    }

};