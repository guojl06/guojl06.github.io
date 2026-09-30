#include "Splash.h"

void Splash::buildMap() {
	char tmp;
	tmp = getchar();
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			tmp = getchar();
			if (tmp == '1' || tmp == '2' || tmp == '3') {
				this->map[i][j] = new Water(tmp - '0', i, j, this);
				// cout << i << ' ' << j << "是 WATER\n";
			}
			else if (tmp == '#') {
				this->map[i][j] = new Void(i, j, this);
				// cout << i << ' ' << j << "是 VOID\n";
			}
			else if (tmp == '*') {
				this->map[i][j] = new Barrier(i, j, this);
				// cout << i << ' ' << j << "是 BARRIER\n";
			}
			else if (tmp == '-') {
				tmp = getchar();
				this->map[i][j] = new Toxic(tmp - '0', i, j, this);
				// cout << i << ' ' << j << "是 TOXIC\n";
			}
			getchar();
		}
	}
}

void Splash::actAt(int x, int y) {
	Object *obj = map[x][y];
	score += obj->act(NONE, PLAYER);
	if(obj != map[x][y]) delete obj;
	return;
}
