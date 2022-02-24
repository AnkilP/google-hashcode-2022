#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using vi = vector<int>;
using pii = pair<int,int>;

vector<string>skill;
map<string,int>mskill;

const int mn = 1e5+10;

struct Collab {
  unordered_map<int,int> skills;
  string name;
  int id;
  int time = 0;
};

struct Project {
  int d,s,b,r;
  vector<pii> req;
  string name;
  vector<Collab*> workers = {};
};

int nc,np;
vector<Collab> cols;
vector<Project> projs;

int bmentor[mn];

bool used[mn];
tuple<vector<Project>,int> solve(vector<Collab> &cols, vector<Project> &projs) {
  vector<Project> sol;
  int score = 0;
  sort(projs.begin(),projs.end(),[](Project&a,Project&b){
    return a.d<b.d;
  });
  deque<Project> q;
  for(Project &p : projs)q.push_back(p);
  while(q.size()){
    Project p = q.front();
    q.pop_front();
    int wt=INT_MIN;
    vector<Collab*> workers;
    bool fail=false;
    for(auto [sk,lv] : p.req) {
      int bt = INT_MAX;
      Collab*bc = nullptr;
      for(Collab&c : cols)if(!used[c.id]) {
        if(c.skills[sk]>=lv||(bmentor[sk]>=lv&&c.skills[sk]>=lv-1)) {
          if(c.time<bt) {
            bt = c.time;
            bc = &c;
          }
        }
      }
      if(!bc) {
        fail=true;
        break;
      }
      for(auto [sk,lv] : bc->skills) {
        bmentor[sk] = max(bmentor[sk],lv);
      }
      workers.push_back(bc);
      wt=max(wt,bt);
      used[bc->id]=true;
    }
    for(Collab *c : workers) {
      used[c->id]=false;
      for(auto [sk,lv] : c->skills) {
        bmentor[sk] = 0;
      }
    }
    if(fail){
      continue;
    }
    if(wt+p.d<p.b+p.s){
      p.workers = workers;
      score += min(p.s,p.b+p.s-wt-p.d);
      for(int i=0; i<p.req.size(); i++) {
        Collab*c = workers[i];
        c->time = wt+p.d;
        int sk = p.req[i].first;
        int lv = p.req[i].second;
        if(c->skills[sk]<=lv) {
          c->skills[sk]++;
        }
      }
      sol.push_back(p);
    }
    else {
      // LOL DIE
      
    }
  }
  return {sol, score};
}

int main() {
  cin.tie(0);
  cin.sync_with_stdio(0);
  
  cin >> nc >> np;
  for(int i=0;i<nc;i++){
    string s;
    cin >> s;
    int k;
    cin >> k;
    unordered_map<int,int> skills;
    for(int j=0;j<k;j++){
      string t;
      cin >> t;
      int ti;
      if(mskill.count(t))ti=mskill[t];
      else{
        ti=skill.size();
        skill.push_back(t);
        mskill[t]=ti;
      }
      int lv;
      cin >> lv;
      skills[ti]=lv;
    }
    cols.push_back({skills,s,i});
  }
  for(int i=0;i<np;i++){
    string name;
    cin >> name;
    int d,s,b,r;
    cin >> d >> s >> b >> r;
    vector<pii> req;
    for(int j=0;j<r;j++){
      string t;
      cin >> t;
      int ti = mskill[t];
      int lv;
      cin >> lv;
      req.push_back({ti,lv});
    }
    projs.push_back({d,s,b,r,req,name});
  }
  ofstream f("out.txt", ios::app);
  auto [sol, score] = solve(cols, projs);
  f << score << "\n";
  printf("%d\n",sol.size());
  for(Project &p : sol) {
    printf("%s\n",p.name.c_str());
    for(Collab *c : p.workers) {
      printf("%s ",c->name.c_str());
    }
    printf("\n");
  }
}
