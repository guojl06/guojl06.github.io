#include "tarnished.h"
#include<iostream>
using namespace std;

Tarnished::Tarnished(){
    for(int i=0;i<MAX_STONES;i++){
        normal_smithing_stones[i]=nullptr;
        somber_smithing_stones[i]=nullptr;
    }
    for(int i=0;i<MAX_WEAPONS;i++){
        normal_weapons[i]=nullptr;
        somber_weapons[i]=nullptr;
    }
    return;
}

Tarnished::~Tarnished(){
    for(int i=1;i<MAX_STONES;i++){
        if(normal_smithing_stones[i]!=nullptr)
            delete normal_smithing_stones[i];
    }
    for(int i=1;i<MAX_STONES;i++){
        if(somber_smithing_stones[i]!=nullptr){
            // cout << "test somber stone delete "<<i<<"\n";
            delete somber_smithing_stones[i];
        }
    }
    for(int i=0;i<MAX_WEAPONS;i++){
        if(normal_weapons[i]!=nullptr)
            delete normal_weapons[i];
    }
    for(int i=0;i<MAX_WEAPONS;i++){
        if(somber_weapons[i]!=nullptr)
            delete somber_weapons[i];
    }
}

void Tarnished::pick_up_weapon(int type, string name){
    if(type==0){
        for(int i=0;i<MAX_WEAPONS;i++){
            if(normal_weapons[i]==nullptr){
                normal_weapons[i] = new NormalWeapon(name);
                return;
            }
                
        }
    }
    else{
        for(int i=0;i<MAX_WEAPONS;i++){
            if(somber_weapons[i]==nullptr){
                somber_weapons[i] = new SomberWeapon(name);
                return;
            }         
        }
    }
}

void Tarnished::pick_up_stone(int type,int level, int number){
    if(type==0){
        if(normal_smithing_stones[level]==nullptr)
            normal_smithing_stones[level] = new NormalSmithingStone(level);
        normal_smithing_stones[level]->change_amount(number);
    }
    else{
        if(somber_smithing_stones[level]==nullptr)
            somber_smithing_stones[level] = new SomberSmithingStone(level);
        somber_smithing_stones[level]->change_amount(number);
    }
}

void Tarnished::upgrade_weapon(int target, string name){
    for(int i=0;i<MAX_WEAPONS;i++){
        // cout << "test " << i << '\n';
        //normal
        if(normal_weapons[i]!=nullptr && normal_weapons[i]->gN()==name){
            // cout << "intest " << i << '\n';
            NormalWeapon *w=normal_weapons[i];
            if(target <= w->gL()){
                cout << "Stay calm!\n";return;
            }
            int level = w->gL();
            // cout << "intest " << i << '\n';
            for(int j=level+1;j<=target;j++){
                if(j%3==0){
                    if(normal_smithing_stones[j/3]==nullptr || normal_smithing_stones[j/3]->get_number() < 6 + 4 * ((j-1)>level) +2 * ((j-2)>level)){
                        cout << "Upgrade failed for lacking normal smithing stone " <<j/3<<".\n";
                        return;
                    }
                    continue;
                }
                else if(j%3==1){
                    if( normal_smithing_stones[(j+2)/3]==nullptr ||normal_smithing_stones[(j+2)/3]->get_number() < 2 )
                    {
                        cout << "Upgrade failed for lacking normal smithing stone " <<(j+2)/3<<".\n";
                        return;
                    }
                    continue;
                }
                else if( normal_smithing_stones[(j+1)/3]==nullptr ||normal_smithing_stones[(j+1)/3]->get_number() < 4 + 2 * ((j-1)>level ))
                {    cout << "Upgrade failed for lacking normal smithing stone "<<(j+(3-j%3))/3<<".\n";
                    return;
                }
            }
            for(int j=level+1;j<=target;j++){
                
                if(j%3==0){
                    normal_smithing_stones[j/3]->change_amount(-6);
                    if(normal_smithing_stones[j/3]->get_number()<=0){
                        delete normal_smithing_stones[j/3];
                        normal_smithing_stones[j/3]=nullptr;
                    }
                    w->upg();
                    
                    if(j-1!=0)
                        cout << "Normal weapon " << w->gN() << "+" << j-1 << " was upgraded to "<<w->gN() << "+" << j <<".\n";
                    else
                        cout << "Normal weapon " << w->gN()  << " was upgraded to "<<w->gN() << "+" << j <<".\n";
                    
                        
                }
                else{
                    
                    normal_smithing_stones[(j+(3-j%3))/3]->change_amount(-(j%3)*2);
                    if(normal_smithing_stones[(j+(3-j%3))/3]->get_number()<=0){
                        delete normal_smithing_stones[(j+(3-j%3))/3];
                        normal_smithing_stones[(j+(3-j%3))/3]=nullptr;
                    }
                    w->upg();
                    
                    if(j-1!=0)
                        cout << "Normal weapon " << w->gN() << "+" << j-1 << " was upgraded to "<<w->gN() << "+" << j <<".\n";
                    else
                        cout << "Normal weapon " << w->gN()  << " was upgraded to "<<w->gN() << "+" << j <<".\n";
                    
                    
                        
                }
                
            }
            if(level!=0)
                cout << "Upgrade "<< w->gN() << "+" << level <<" to "<<w->gN()<<"+"<<w->gL()<<" Successfully.\n";
            else
                cout << "Upgrade "<< w->gN() <<" to "<<w->gN()<<"+"<<w->gL()<<" Successfully.\n";
            return;
        }

        //somber
        else{
            if(somber_weapons[i]!=nullptr && somber_weapons[i]->gN()==name){
                SomberWeapon *w = somber_weapons[i];
                if(target <= w->gL()){
                    cout << "Stay calm!\n";return;
                }
                int level = w->gL();
                for(int j=level+1;j<=target;j++){
                    if(somber_smithing_stones[j]==nullptr || somber_smithing_stones[j]->get_number()<1){
                        cout << "Upgrade failed for lacking somber smithing stone "<< j <<".\n";return;
                    }
                }
                for(int j=level+1;j<=target;j++){
                    somber_smithing_stones[j]->change_amount(-1);
                    if(somber_smithing_stones[j]->get_number()<=0){
                        delete somber_smithing_stones[j];
                        // ！！！！！  必须手动置空！！！
                        somber_smithing_stones[j]=nullptr;
                        // if(somber_smithing_stones[j]==nullptr) cout << "Yes\n";
                        // else cout << "No!\n";
                    }
                    w->upg();
                    if(j-1!=0)
                        cout << "Somber weapon " << w->gN() << "+" << j-1 << " was upgraded to "<<w->gN() << "+" << j <<".\n";
                    else   
                        cout << "Somber weapon " << w->gN()  << " was upgraded to "<<w->gN() << "+" << j <<".\n";   
                }

                if(level!=0)
                    cout << "Upgrade "<< w->gN() << "+" << level <<" to "<<w->gN()<<"+"<<w->gL()<<" Successfully.\n";
                else
                    cout << "Upgrade "<< w->gN() <<" to "<<w->gN()<<"+"<<w->gL()<<" Successfully.\n";
                return;
            }
        }
    }
    cout << "You don't have the right!\n";
}