/*
A war game is conducted between two countries A and B. Country A at its Air Force Base in Rimnicu Vilcea has some Rockwell B-1 Lancer Heavy Bombers and some Mitsubishi F-3 Fighters. Since bombers are comparatively slow and are not easily maneuverable each bomber should be accompanied by at least a squadron of three fighters. Rimnicu Vilcea Air Force Base has over 5000 liter of fuel, 200 pilots, 4 wing commanders and an Air Marshal. Moreover, enemy airfields of Sibiu and Fagaras are within reach of the bombers from Rimnicu Vilcea. So, airfields of Rimnicu Vilcea should remain operational, it is vital for winning the war. According to Air Marshal Prince Constantin Cantacuzino, “we need at least 10 fighters in the air to defend against their first wave of attack”.

Assume that both Rockwell B-1 Lancer Heavy Bomber and Mitsubishi F-3 Fighter can be operated by a single pilot. Assume that all the pilots, wing commanders and Air Marshal are competent pilots but due tactical reasons Air Marshals is not allowed to participate in any flying missions.

Can you write a C program to read the number of fighters and bombers from the user and identify the maximum numbers Rockwell B-1 Heavy Bombers that can be sent on a bombing run at a time by country A so that airfields of Rimnicu Vilcea won’t be vulnerable to air raids from Country B’s bombers?

You have input the number of fighter first followed by the number of bombers.

Sample Input/Output
    Input:
    0 0
    Output
    0
*/
//Ans
#include <stdio.h>
int main(){
    int v_f3_def=10; //first wave defense
    int v_inp_f3=0;//input number of f3 fighters
    int v_inp_hb=0;//inp number of heavy bombers
    int v_pilots=204;
    int v_out_f3=0;
    int v_out_hb=0;
    //int n=0;
    scanf("%d %d",&v_inp_f3,&v_inp_hb);
    if(v_inp_f3>v_pilots) {
        v_inp_f3=v_pilots;//max number of pilots excluding Air marshal
    }else if(v_inp_f3<0){
        v_inp_f3=0;
    } 
    if (v_inp_hb>204){
        v_inp_hb=v_pilots;
    } else if (v_inp_hb<0){
        v_inp_hb=0;
    }
    v_inp_f3=v_inp_f3-v_f3_def;
    v_pilots=v_pilots-v_f3_def;
    if (v_inp_f3<=0){
        v_out_hb=0;
    } else if (v_inp_hb<=0){
         v_out_hb=0;
    }
    else{
    if(v_inp_f3>0 && v_inp_hb>0){
        while(v_inp_f3/3>0 && v_inp_hb>0 && v_pilots>3){
            if(v_inp_f3>0 && v_inp_hb>0&& v_pilots>3){
            v_inp_f3=v_inp_f3-3;
            v_inp_hb=v_inp_hb-1;
            v_pilots=v_pilots-4;
            ++v_out_hb;
           ;
            }
        }
    }
    }
printf("%d",v_out_hb);
    return 0;
}
