int a = 0;

int main (){
    bool c = a>0 && false || a < 0;
    
    if (a > 0 && false || a < 0) {
        c = true;
    }

    return 0;
}