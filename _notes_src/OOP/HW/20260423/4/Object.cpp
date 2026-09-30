#include "Object.h"
#include "Splash.h"

Dir DIRE[4]={
	{-1,0,UP},
	{1,0,DOWN},
	{0,-1,LEFT},
	{0,1,RIGHT}
};
string STR[5]={"","LEFT","RIGHT","UP","DOWN"};

Water::Water(int val,int mx,int my,Splash* msplash){
    value=val,x=mx,y=my,splash=msplash;
}
int Water::act(Direction fromwhere, Actor fromwho){
    // cout << "现在是 WATER " << x << ' ' << y << "\n";
    if(fromwho==PLAYER) return act(fromwhere,WATER);
    if(fromwho==TOXIC){
        --value;
        if(value==0) splash->map[x][y]=new Void(x,y,splash);
        return 0;
    }
    // int tot=1;
    if(fromwho==WATER){
        
        if((++value)<=3) return 0;
        splash->map[x][y]=new Void(x,y,splash);
        // cout << "WATER " << x << ' ' << y << " 爆了\n";
        
        for(int i=0;i<4;i++){
            // if((DIRE[i].dir+fromwhere==3 && fromwhere!=NONE) || (DIRE[i].dir+fromwhere==7))
            //     continue;
            int tx=x+DIRE[i].x,ty=y+DIRE[i].y;
            
            if(tx >=0 && tx < splash->size && ty>=0 && ty< splash->size){
                // cout << "WATER " << x << ' ' << y << " 爆 " << tx << ' ' << ty << '\n';
                Object *obj=splash->map[tx][ty];
                obj->act(DIRE[i].dir,WATER);
                // cout << "WATER " << x << ' ' << y << " 爆 " << tx << ' ' << ty << "结束\n";
                if(obj != splash->map[tx][ty]) delete obj;
            }
        }

        // cout << "WATER " << x << ' ' << y << " 贡献1" << '\n';
        
    }
    splash->score++;
    // cout << "WATER " << x << ' ' << y << "  分数 " << splash->score << '\n';
    return 0;

}

Toxic::Toxic(int val,int mx,int my,Splash* msplash){
    value=val,x=mx,y=my,splash=msplash;
}
int Toxic::act(Direction fromwhere, Actor fromwho){
    // cout << "TOXIC " << x << ' ' << y << "  触发 " << '\n';
    if(fromwho==PLAYER) return act(fromwhere,TOXIC);
    if(fromwho==WATER){
        --value;
        if(value==0) splash->map[x][y]=new Void(x,y,splash);
        return 0;
    }
    // int tot=-1;
    if(fromwho==TOXIC){
        if(++value<=3) return 0;
        splash->map[x][y]=new Void(x,y,splash);
        for(int i=0;i<4;i++){
            // if((DIRE[i].dir+fromwhere==3 && fromwhere!=NONE) || (DIRE[i].dir+fromwhere==7))
            //     continue;
            int tx=x+DIRE[i].x,ty=y+DIRE[i].y;
            if(tx >=0 && tx < splash->size && ty>=0 && ty< splash->size){
                Object *obj=splash->map[tx][ty];
                obj->act(DIRE[i].dir,TOXIC);
                if(obj != splash->map[tx][ty]) delete obj;
            }
        }
        // cout << "TOXIC " << x << ' ' << y << " 贡献-1" << '\n';
        
    }
    splash->score--;
    return 0;
}

Void::Void(int mx,int my,Splash* msplash){
    x=mx,y=my,splash=msplash;
}
int Void::act(Direction fromwhere, Actor fromwho){
    if(fromwho==PLAYER) cout << "Error: Cannot act a Void.\n";
    else{
        // cout << "Void " << x << ' ' << y << " 路过 " << '\n';
        for(int i=0;i<4;i++){
            int tx=x+DIRE[i].x,ty=y+DIRE[i].y;
            if(fromwhere==DIRE[i].dir && tx >=0 && tx < splash->size && ty>=0 && ty< splash->size){
                // cout << "Void " << x << ' ' << y << " 方向 " << STR[fromwhere] << '\n';
                Object *obj=splash->map[tx][ty];
                obj->act(DIRE[i].dir,fromwho);
                if(obj != splash->map[tx][ty]) delete obj;
                break;
            }
        }
    }
    return 0;
}

Barrier::Barrier(int mx,int my,Splash* msplash){
    x=mx,y=my,splash=msplash;
}
int Barrier::act(Direction fromwhere, Actor fromwho){
    if(fromwho==PLAYER) cout << "Error: Cannot act a Barrier.\n";
    return 0;
}

/*
 * ======================= 十滴水 (Splash) 避坑指南 =======================
 * 1. 爆炸方向顺序 (Order Matters): 
 * 题目明确要求按“上、下、左、右”顺序处理。必须保证 DIRE 数组索引 0-3 严格对应 
 * UP, DOWN, LEFT, RIGHT，且循环触发 act 时不可打乱此顺序。
 * * 2. 溅射不回流陷阱 (No Reflection Filter):
 * 严禁在 act 函数中使用 (DIRE[i].dir + fromwhere == constant) 之类的逻辑来
 * 过滤“反方向”。爆炸是全向喷射的，即使是触发它的那个方向也要喷回去。
 * * 3. 分数计算时机 (Score Timing):
 * 分数增加 (score++) 必须在进入四个方向的递归循环之前执行。
 * 这样可以保证在深层连锁反应发生前，当前的爆炸得分已正确入账。
 * * 4. 毒液数值逻辑 (Toxic Value Logic):
 * 题目中毒液是 -1, -2, -3。若你存储的是绝对值(1, 2, 3)，则：
 * - 玩家操作/毒液溅射 -> value++ (变大)
 * - 水滴溅射到毒液 -> value-- (变小)
 * 若 value 减小到 0，毒液消失但不扣分；若 value 增大超过 3，毒液爆炸扣 1 分。
 * * 5. 内存安全与对象替换 (Pointer Safety):
 * 当一个对象爆开或消失变成 Void 时，splash->map[x][y] 指向了新对象。
 * 在递归返回后，必须通过 (obj != splash->map[tx][ty]) 判断旧对象是否已被替换，
 * 若是，则必须 delete obj 以防内存泄漏。
 * * 6. Void 穿透逻辑 (Void Propagation):
 * Void::act 必须起到“透镜”作用，将溅射沿原方向(fromwhere)传导至下一个格子，
 * 不能改变方向，也不能在 fromwho == PLAYER 时允许操作。
 * ========================================================================
 */