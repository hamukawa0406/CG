#include <math.h>
#include <string>
#include <iostream>
#include <glut.h>
#include <ctype.h>

using namespace std;

const float MTXLIB_PI = 3.14159265f;
/**
 * 3次元ベクトル構造体
 */
struct Vec3
{
	float x, y, z;
	Vec3(float x=0, float y=0, float z=0){this->x=x; this->y=y; this->z=z;}
	Vec3 operator +(Vec3 &vec)           {return Vec3(this->x+vec.x, this->y+vec.y, this->z+vec.z);}
	Vec3 operator -(Vec3 &vec)           {return Vec3(this->x-vec.x, this->y-vec.y, this->z-vec.z);}
	Vec3 operator *(float f)             {return Vec3(this->x*f, this->y*f, this->z*f);}
	Vec3 operator /(float f)             {return Vec3(this->x/f, this->y/f, this->z/f);}
	Vec3 operator =(Vec3 &vec)           {return Vec3(this->x=vec.x, this->y=vec.y, this->z=vec.z);}
	Vec3 operator ==(Vec3 &vec)          {return (this->x==vec.x && this->y==vec.y && this->z==vec.z);}
	Vec3 operator !=(Vec3 &vec)          {return (this->x!=vec.x || this->y!=vec.y || this->z!=vec.z);}
	void Set(float x, float y, float z)  {this->x=x; this->y=y; this->z=z;}
	// スカラの二乗を求める
	float LengthSq() {return x*x + y*y + z*z;}
	// スカラ
	float Length() {return (float)sqrt(LengthSq());}
	// 正規化
	Vec3 Normalize() {
		float m = LengthSq();
		if (m > 0.0f) m = 1.0f / m;
		else          m = 0.0f;
		return Vec3(x*m, y*m, z*m);
	}
	// 内積
	float Dot(Vec3 &vec)
	{
		return (this->x*vec.x + this->y*vec.y + this->z*vec.z);
	}
	// 外積
	Vec3 Cross(Vec3 &vec)
	{
		return Vec3(
			this->y*vec.z - this->z*vec.y,
			this->z*vec.x - this->x*vec.z,
			this->x*vec.y - this->y*vec.x);
	}
	string Debug()
	{
		char tmp[256];
		sprintf(tmp, "(x,y,z)=(%f,%f,%f", x, y, z);
		string ret = tmp;
		return ret;
	}
};

/**
 * 4次元ベクトル構造体
 */
struct Vec4
{
	float x, y, z, w;
	Vec4(float x=0, float y=0, float z=0, float w=0){this->x=x; this->y=y; this->z=z; this->w=w;}
	Vec4 operator +(Vec4 &vec)           {return Vec4(this->x+vec.x, this->y+vec.y, this->z+vec.z, this->w+vec.w);}
	Vec4 operator -(Vec4 &vec)           {return Vec4(this->x-vec.x, this->y-vec.y, this->z-vec.z, this->w-vec.w);}
	Vec4 operator *(float f)             {return Vec4(this->x*f, this->y*f, this->z*f, this->w*f);}
	Vec4 operator /(float f)             {return Vec4(this->x/f, this->y/f, this->z/f, this->w/f);}
	Vec4 operator =(Vec4 &vec)           {return Vec4(this->x=vec.x, this->y=vec.y, this->z=vec.z, this->w=vec.w);}
	Vec4 operator ==(Vec4 &vec)          {return (this->x==vec.x && this->y==vec.y && this->z==vec.z && this->w==vec.w);}
	Vec4 operator !=(Vec4 &vec)          {return (this->x!=vec.x || this->y!=vec.y || this->z!=vec.z || this->w!=vec.w);}
	void Set(float x, float y, float z, float w)  {this->x=x; this->y=y; this->z=z; this->w=w;}
	void Set(int i, float param)
	{
		if(i == 0)      x = param;
		else if(i == 1) y = param;
		else if(i == 2) z = param;
		else if(i == 3) w = param;
	}
	float Get(int i)
	{
		if(i == 0)      return x;
		else if(i == 1) return y;
		else if(i == 2) return z;
		else if(i == 3) return w;
		else            return 0;
	}
	// スカラの二乗を求める
	float LengthSq() {return x*x + y*y + z*z + w*w;}
	// スカラ
	float Length() {return sqrt(LengthSq());}
	// 正規化
	Vec4 Normalize() {
		float m = LengthSq();
		if (m > 0.0f) m = 1.0f / m;
		else          m = 0.0f;
		return Vec4(x*=m, y*=m, z*=m, w*=m);
	}
	// 内積
	float Dot(Vec4 &vec)
	{
		return (this->x*vec.x + this->y*vec.y + this->z*vec.z + this->w*vec.w);
	}
};

/**
 * 4×4行列構造体
 */
struct Mat44
{
	Vec4 col[4];
	Mat44(Vec4 v0=Vec4(1,0,0,0), Vec4 v1=Vec4(0,1,0,0), Vec4 v2=Vec4(0,0,1,0), Vec4 v3=Vec4(0,0,0,1))
	{
		col[0] = v0; col[1] = v1; col[2] = v2; col[3] = v3;
	}
	Mat44 operator *(Mat44 &m) 
	{
		Mat44 t;
		for (int r = 0; r < 4; r++)
		{
			for (int c = 0; c < 4; c++)
			{
				float f = 0;

				f += (Get(0, r) * m.Get(c, 0));
				f += (Get(1, r) * m.Get(c, 1));
				f += (Get(2, r) * m.Get(c, 2));
				f += (Get(3, r) * m.Get(c, 3));

				t.Set(c, r, f);
			}
		}
		return t;
	}
	Vec3 operator *(Vec3 &v)
	{
		Vec3 ret;
		ret.x = (v.x * this->col[0].x) + (v.y * this->col[1].x) + (v.z * this->col[2].x) + (this->col[3].x);
		ret.y = (v.x * this->col[0].y) + (v.y * this->col[1].y) + (v.z * this->col[2].y) + (this->col[3].y);
		ret.z = (v.x * this->col[0].z) + (v.y * this->col[1].z) + (v.z * this->col[2].z) + (this->col[3].z);
		return ret;
	}
	Vec4 operator *(Vec4 &v)
	{
		Vec4 ret;
		ret.x = v.x * this->col[0].x + v.y * this->col[1].x + v.z * this->col[2].x + v.w * this->col[3].x;
		ret.y = v.x * this->col[0].y + v.y * this->col[1].y + v.z * this->col[2].y + v.w * this->col[3].y;
		ret.z = v.x * this->col[0].z + v.y * this->col[1].z + v.z * this->col[2].z + v.w * this->col[3].z;
		ret.w = v.x * this->col[0].w + v.y * this->col[1].w + v.z * this->col[2].w + v.w * this->col[3].w;
		return ret;
	}
	float Get(int c, int r) {return col[c].Get(r);}
	void Set(int c, int r, float i) {col[c].Set(r, i);}
	// 単位行列
	Mat44 Identity()
	{
		return Mat44(Vec4(1,0,0,0), Vec4(0,1,0,0), Vec4(0,0,1,0), Vec4(0,0,0,1));
	}
	// 平行移動に変換
	Mat44 Translate(float x, float y, float z)
	{
		Mat44 ret;
		ret = ret.Identity();
		ret.col[3].x = x;
		ret.col[3].y = y;
		ret.col[3].z = z;
		return ret;
	}
	Mat44 Translate(Vec3 v)
	{
		Mat44 ret;
		ret = ret.Identity();
		ret.col[3].x = v.x;
		ret.col[3].y = v.y;
		ret.col[3].z = v.z;
		return ret;
	}
	// 回転行列に変換
	Mat44 Rotate(char axis, float rad)
	{
		Mat44 ret;
		float sinA = sinf(rad);
		float cosA = cosf(rad);
		switch (axis)
		{
		case 'x':
		case 'X':
			ret.col[0].x =  1.0F; ret.col[1].x =  0.0F; ret.col[2].x =  0.0F;
			ret.col[0].y =  0.0F; ret.col[1].y =  cosA; ret.col[2].y = -sinA;
			ret.col[0].z =  0.0F; ret.col[1].z =  sinA; ret.col[2].z =  cosA;
			break;

		case 'y':
		case 'Y':
			ret.col[0].x =  cosA; ret.col[1].x =  0.0F; ret.col[2].x =  sinA;
			ret.col[0].y =  0.0F; ret.col[1].y =  1.0F; ret.col[2].y =  0.0F;
			ret.col[0].z = -sinA; ret.col[1].z =  0.0F; ret.col[2].z =  cosA;
			break;

		case 'z':
		case 'Z':
			ret.col[0].x =  cosA; ret.col[1].x = -sinA; ret.col[2].x =  0.0F;
			ret.col[0].y =  sinA; ret.col[1].y =  cosA; ret.col[2].y =  0.0F;
			ret.col[0].z =  0.0F; ret.col[1].z =  0.0F; ret.col[2].z =  1.0F;
			break;
		}

		ret.col[0].w = 0.0F; ret.col[1].w = 0.0F; ret.col[2].w = 0.0F;
		ret.col[3].x = 0.0F;
		ret.col[3].y = 0.0F;
		ret.col[3].z = 0.0F;
		ret.col[3].w = 1.0F;

		return ret;
	}
	// YawPitchRollを指定して回転行列を取得
	Mat44 YawPitchRoll(float y, float x, float z)
	{
		Mat44 ret;
		Mat44 mY = ret.Rotate('y', y);
		Mat44 mX = ret.Rotate('x', x);
		Mat44 mZ = ret.Rotate('z', z);
		return mZ*mX*mY;
	}
	// 拡大・縮小行列に変換
	Mat44 Scale(float x, float y, float z)
	{
		Mat44 ret;

		ret = ret.Identity();
		ret.col[0].x = x;
		ret.col[1].y = y;
		ret.col[2].z = z;

		return ret;
	}
};

// 角度をラジアンに変換
float DegToRad(float deg)
{
	return deg*MTXLIB_PI/180;
}

/**
 * 箱構造体
 */
struct TCube
{
	Vec3 pos;    // 中心座標
	Vec3 radius; // 半径
	Vec3 rot;    // 回転角度
	Vec3 axisX;  // 分離軸X
	Vec3 axisY;  // 分離軸Y
	Vec3 axisZ;  // 分離軸Z
	Vec3 GetMinVec3()
	{
		return Vec3(
			pos.x-radius.x,
			pos.y-radius.y,
			pos.z-radius.z);
	}
	Vec3 GetMaxVec3()
	{
		return Vec3(
			pos.x+radius.x,
			pos.y+radius.y,
			pos.z+radius.z);
	}
	// 分離軸を更新
	void UpdateAxisAll()
	{
		Mat44 mRot = Mat44().YawPitchRoll(DegToRad(rot.y), DegToRad(rot.x), DegToRad(rot.z));
		axisX = mRot*Vec3(1, 0, 0);
		axisY = mRot*Vec3(0, 1, 0);
		axisZ = mRot*Vec3(0, 0, 1);
	}
};

bool CompareLengthOBB(TCube&, TCube&, Vec3, Vec3);
/**
 * 境界箱（OBB）による当たり判定
 * @return 衝突していたらtrue
 */
bool IsCollideBoxOBB(TCube cA, TCube cB)
{
	// 中心間の距離ベクトル算出
	Vec3 vDistance = cB.pos - cA.pos;

	// 分離軸更新
	cA.UpdateAxisAll();
	cB.UpdateAxisAll();

	// 分離軸を比較
	if(!CompareLengthOBB(cA, cB, cA.axisX, vDistance)) return false;
	if(!CompareLengthOBB(cA, cB, cA.axisY, vDistance)) return false;
	if(!CompareLengthOBB(cA, cB, cA.axisZ, vDistance)) return false;
	if(!CompareLengthOBB(cA, cB, cB.axisX, vDistance)) return false;
	if(!CompareLengthOBB(cA, cB, cB.axisY, vDistance)) return false;
	if(!CompareLengthOBB(cA, cB, cB.axisZ, vDistance)) return false;

	// 分離軸同士の外積を比較
	Vec3 vSep;
	vSep = cA.axisX.Cross(cB.axisX);
	if(!CompareLengthOBB(cA, cB, vSep, vDistance)) return false;
	vSep = cA.axisX.Cross(cB.axisY);
	if(!CompareLengthOBB(cA, cB, vSep, vDistance)) return false;
	vSep = cA.axisX.Cross(cB.axisZ);
	if(!CompareLengthOBB(cA, cB, vSep, vDistance)) return false;
	vSep = cA.axisY.Cross(cB.axisX);
	if(!CompareLengthOBB(cA, cB, vSep, vDistance)) return false;
	vSep = cA.axisY.Cross(cB.axisY);
	if(!CompareLengthOBB(cA, cB, vSep, vDistance)) return false;
	vSep = cA.axisY.Cross(cB.axisZ);
	if(!CompareLengthOBB(cA, cB, vSep, vDistance)) return false;
	vSep = cA.axisZ.Cross(cB.axisX);
	if(!CompareLengthOBB(cA, cB, vSep, vDistance)) return false;
	vSep = cA.axisZ.Cross(cB.axisY);
	if(!CompareLengthOBB(cA, cB, vSep, vDistance)) return false;
	vSep = cA.axisZ.Cross(cB.axisZ);
	if(!CompareLengthOBB(cA, cB, vSep, vDistance)) return false;

	return true;
}

/**
 * OBBの投影距離比較
 * @return 衝突していたらtrue
 */
bool CompareLengthOBB(TCube &cA, TCube &cB, Vec3 vSep, Vec3 vDistance)
{
	// 分離軸上のAからBの距離
	float length = fabsf(vSep.Dot(vDistance));

	// 分離軸上でAから最も遠いAの頂点までの距離
	float lenA = 
		  fabsf(cA.axisX.Dot(vSep)*cA.radius.x)
		  + fabsf(cA.axisY.Dot(vSep)*cA.radius.y)
		  + fabsf(cA.axisZ.Dot(vSep)*cA.radius.z);

	// 分離軸上でBから最も遠いBの頂点までの距離
	float lenB = 
		  fabsf(cB.axisX.Dot(vSep)*cB.radius.x)
		  + fabsf(cB.axisY.Dot(vSep)*cB.radius.y)
		  + fabsf(cB.axisZ.Dot(vSep)*cB.radius.z);
	if(length > lenA + lenB)
	{
		return false;
	}
	return true;
}

/**
 * 箱の描画
 */
void DrawCube(Vec3 pos, Vec3 radius, Vec3 rot, int color)
{
	// シーンの描画
	static GLfloat red[]   = { 0.8, 0.2, 0.2, 1.0 };
	static GLfloat gleen[] = { 0.2, 0.8, 0.2, 1.0 };
	static GLfloat white[] = { 0.8, 0.8, 0.8, 1.0 };
	GLfloat *c;
	if(color == 0)      c = red;
	else if(color == 1) c = gleen;
	else                c = white;

	// 陰影付けをONにする
	glEnable(GL_LIGHTING);
	// 箱描画
	glPushMatrix();
	{
		glTranslatef(pos.x, pos.y, pos.z);
		glRotatef(rot.z, 0, 0, 1);
		glRotatef(rot.x, 1, 0, 0);
		glRotatef(rot.y, 0, 1, 0);
		glScaled(radius.x*2, radius.y*2, radius.z*2);
		glMaterialfv(GL_FRONT, GL_DIFFUSE, c);
		glutSolidCube(1);
	}
	glPopMatrix();
	// 陰影付けをOFFにする
	glDisable(GL_LIGHTING);
}

TCube self;   // 箱１（コイツが動く）
TCube target; // 箱２（コイツは動かない）

Vec3 vEye;    // カメラ座標
bool bHit;    // 当たりフラグ

/**
 * 初期化
 */
void Init(void)
{
	// 初期設定
	glClearColor(0.0, 0.0, 1.0, 0.0);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);
	glEnable(GL_LIGHT0);

	// 箱を作る
	self.pos      = Vec3(1, 0, 0);
	self.radius   = Vec3(0.4f, 0.5f, 0.6f);
	self.rot      = Vec3(0, 0, 0);
	target.pos    = Vec3(0, 0, 0);
	target.radius = Vec3(0.5f, 0.6f, 0.4f);
	target.rot    = Vec3(30, 45, 60);

	// カメラ座標初期化
	vEye = Vec3(0, 0, -5);

	bHit = false;
}

/**
 * キーが押されたときの処理
 * @param key  押下キー
 * @param x, y 座標
 */
void InputKey(unsigned char key, int x, int y)
{
	// 動かす
	float mov = 0.1f;
	float rot = 1;
	Mat44 mRot;
	switch(toupper(key))
	{
	case 'Z':
		self.pos.x += mov;
		break;
	case 'X':
		self.pos.x -= mov;
		break;
	case 'A':
		self.pos.y += mov;
		break;
	case 'S':
		self.pos.y -= mov;
		break;
	case 'Q':
		self.pos.z += mov;
		break;
	case 'W':
		self.pos.z -= mov;
		break;
	case 'C':
		self.rot.x -= rot;
		break;
	case 'V':
		self.rot.x += rot;
		break;
	case 'D':
		self.rot.y -= rot;
		break;
	case 'F':
		self.rot.y += rot;
		break;
	case 'E':
		self.rot.z -= rot;
		break;
	case 'R':
		self.rot.z += rot;
		break;
	case 0x1b:	// ＥＳＣキー
		// プログラムを終了
		exit(0);
		break;
	}
	if(self.rot.x < 0)   self.rot.x += 360;
	if(self.rot.x > 360) self.rot.x -= 360;
	if(self.rot.y < 0)   self.rot.y += 360;
	if(self.rot.y > 360) self.rot.y -= 360;
	if(self.rot.z < 0)   self.rot.z += 360;
	if(self.rot.z > 360) self.rot.z -= 360;

	// 当たり判定
	if(IsCollideBoxOBB(self, target))
	{
		bHit = true;
	}
	else
	{
		bHit = false;
	}
}

/**
 * 特殊キーが押されたときの処理
 * @param key  押下キー
 * @param x, y 座標
 */
void InputKeySp(int key, int x, int y)
{
	// カメラ移動
	Vec3 vAxis;
	Vec3 vN;
	switch(key)
	{
	case GLUT_KEY_UP:
		// 上キー
		vAxis = Vec3(-1, 0, 0);
		break;
	case GLUT_KEY_DOWN:
		// 下キー
		vAxis = Vec3(1, 0, 0);
		break;
	case GLUT_KEY_LEFT:
		// 左キー
		vAxis = Vec3(0, 1, 0);
		break;
	case GLUT_KEY_RIGHT:
		// 右キー
		vAxis = Vec3(0, -1, 0);
		break;
	}
	vN = vEye.Normalize().Cross(vAxis);
	vEye = vEye + vN;
}

/**
 * 描画
 */
void Display(void)
{
	// 画面クリア
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// 視点の移動
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	gluLookAt(vEye.x, vEye.y, vEye.z, 0, 0, 0, 0, 1, 0);

	// 箱の描画
	if(bHit) DrawCube(self.pos, self.radius, self.rot, 0);
	else     DrawCube(self.pos, self.radius, self.rot, 2);
	DrawCube(target.pos, target.radius, target.rot, 1);

	// 地面を線画で描く
	glColor3d(0.0, 0.0, 0.0);
	glBegin(GL_LINES);
	{
		for (int i = -10; i <= 10; i++)
		{
			glVertex3d((GLdouble)i, -0.5, -10.0);
			glVertex3d((GLdouble)i, -0.5,  10.0);
			glVertex3d(-10.0, -0.5, (GLdouble)i);
			glVertex3d( 10.0, -0.5, (GLdouble)i);
		}
	}
	glEnd();

	glutSwapBuffers();
}

/**
 * ウィンドウのリサイズ
 */
void Resize(int w, int h)
{
	// ウィンドウ全体をビューポートにする
	glViewport(0, 0, w, h);

	// 透視変換行列を設定する
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	gluPerspective(30.0, (double)w / (double)h, 1.0, 100.0);

	// モデルビュー変換行列を指定しておく
	glMatrixMode(GL_MODELVIEW);
}

/**
 * アイドル時
 */
void Idle()	
{
	glutPostRedisplay();
}

/**
 * メイン関数
 */
int main(int argc, char *argv[])
{
	glutInit(&argc, argv);
	glutInitWindowSize(640, 480); 
	glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH | GLUT_DOUBLE);
	glutCreateWindow(argv[0]);
	glutDisplayFunc(Display);
	glutReshapeFunc(Resize);
	// キーボード入力用関数を登録
	glutKeyboardFunc(InputKey);
	glutSpecialFunc(InputKeySp);
	glutIdleFunc(Idle);
	Init();
	// メインループ
	glutMainLoop();
	return 0;
}