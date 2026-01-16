# -*- coding: utf-8 -*-
import random
import os

LEADERBOARD_FILE = "leaderboard.txt"
MAX_LEADERBOARD_ENTRIES = 5
SCORE_LIMIT = 2000

# Level configuration: Name, Range(1-X), Max attempts, Bonus for clearing
LEVELS = [
    {"name": "L1", "max_number": 50, "max_attempts": 7, "clear_bonus": 50},
    {"name": "L2", "max_number": 100, "max_attempts": 6, "clear_bonus": 100},
    {"name": "L3", "max_number": 200, "max_attempts": 5, "clear_bonus": 200},
]

def calculate_score(attempts, max_attempts):
    score = 100 - (attempts - 1) * 10
    return max(score, 0)

def load_leaderboard():
    entries = []
    if not os.path.exists(LEADERBOARD_FILE):
        return entries
    try:
        with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if ',' in line:
                    name, score = line.rsplit(',', 1)
                    entries.append((name.strip(), int(score.strip())))
    except:
        pass
    entries.sort(key=lambda x: x[1], reverse=True)
    return entries[:MAX_LEADERBOARD_ENTRIES]

def save_leaderboard(entries):
    try:
        with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
            for name, score in entries:
                f.write(f"{name},{score}\n")
    except:
        print("警告：无法保存排行榜。")

def play_level(level_cfg):
    target = random.randint(1, level_cfg["max_number"])
    print(f"\n--- 关卡 {level_cfg['name']} (1-{level_cfg['max_number']}) ---")
    print(f"允许尝试次数：{level_cfg['max_attempts']}")
    
    for attempt in range(1, level_cfg["max_attempts"] + 1):
        try:
            guess = int(input(f"第 {attempt} 次：请输入你的猜测："))
            if guess == target:
                level_score = calculate_score(attempt, level_cfg['max_attempts'])
                print(f"正确！本关得分：{level_score}")
                return True, level_score
            elif guess < target:
                print("太小了！")
            else:
                print("太大了！")
        except ValueError:
            print("请输入数字。")
    print(f"游戏结束！答案是 {target}。")
    return False, 0

def main():
    print("欢迎来到猜数字：关卡模式")
    leaderboard = load_leaderboard()
    
    while True:
        total_score = 0
        cleared_all = True
        for lvl in LEVELS:
            success, score = play_level(lvl)
            if success:
                total_score += score + lvl["clear_bonus"]
                print(f"当前总分：{total_score}")
            else:
                cleared_all = False
                break
        
        print(f"\n游戏结束。最终得分：{total_score}")
        if total_score > 0:
            if not leaderboard or len(leaderboard) < 5 or total_score > leaderboard[-1][1]:
                name = input("新纪录！请输入你的名字：")
                leaderboard.append((name, total_score))
                leaderboard.sort(key=lambda x: x[1], reverse=True)
                leaderboard = leaderboard[:5]
                save_leaderboard(leaderboard)
        
        print("\nTOP 5 排行榜：")
        print("排名\t玩家\t分数")
        for i, (n, s) in enumerate(leaderboard, 1):
            print(f"{i}.\t{n}\t{s}")
            
        if input("\n再玩一次？(y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()
