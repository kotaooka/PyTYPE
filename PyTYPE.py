import os
import random
import time
import configparser

def load_wordlist(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            wordlist = [word.strip() for word in file.readlines()]
    except FileNotFoundError:
        print(f"エラー：{filename} ファイルが見つかりませんでした。")
        exit(1)
    except Exception as e:
        print(f"エラー：{filename} ファイルを読み込めませんでした。エラー内容: {e}")
        exit(1)
    return wordlist

def save_score(filename, player_name, word_count, correct_count):
    config = configparser.ConfigParser()
    if os.path.exists(filename):
        config.read(filename)
    config[player_name] = {
        "TotalWords": str(word_count),
        "CorrectWords": str(correct_count),
    }
    with open(filename, 'w') as configfile:
        config.write(configfile)

def display_leaderboard(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: int(x[1]["CorrectWords"]), reverse=True)
    print("ランキング:")
    for idx, (name, score) in enumerate(sorted_scores[:10], start=1):
        print(f"{idx}位: {name} - 正解数: {score['CorrectWords']}")
    return sorted_scores

def typing_practice(limit_time):
    words = load_wordlist("wordlist.txt")
    total_time = limit_time * 60
    correct_count = 0
    word_count = 0
    start_time = time.time()

    print(f"{limit_time}分間のタイピング練習を開始します。")
    input("Enterキーを押して開始...")
    print()

    while time.time() - start_time < total_time:
        if not words:
            print("単語リストが空になりました。タイピング練習を終了します。")
            break
        target_word = random.choice(words)
        words.remove(target_word)
        print("次の単語を入力してください:", target_word)
        
        typed_word = input("入力してください: ").strip()
        
        if typed_word == target_word:
            correct_count += 1
            print("正解です！", end=' ')
        else:
            print("不正解です。", end=' ')

        word_count += 1
        print("残り時間:", round(total_time - (time.time() - start_time), 2), "秒", end='\n\n')

    print(f"{limit_time}分間のタイピング練習が終了しました！")
    print("総入力単語数:", word_count)
    print("正解数:", correct_count)

    player_name = input("ニックネームを入力してください：")
    past_scores = configparser.ConfigParser()
    past_scores.read("savedata.ini")

    print("過去の記録:")
    if past_scores.sections():
        scores = {}
        for section in past_scores.sections():
            scores[section] = past_scores[section]
        sorted_scores = display_leaderboard(scores)

    if past_scores.has_section(player_name):
        past_correct_words = int(past_scores[player_name]["CorrectWords"])

        print("過去の記録:")
        print("正解数:", past_correct_words)

        rank = sorted_scores.index((player_name, past_scores[player_name])) + 1
        if rank <= 10:
            print(f"おめでとうございます！{rank}位にランクインしました！")
        else:
            print("ランクインできませんでした。")

    save_score("savedata.ini", player_name, word_count, correct_count)

while True:
    print("練習する時間を選択してください：")
    print("1: 1分")
    print("2: 3分")
    print("3: 5分")
    choice = input("選択肢を入力してください：")

    if choice in ["1", "2", "3"]:
        limit_time = int(choice)
        break
    else:
        print("無効な選択です。1から3の間で選んでください。")

typing_practice(limit_time)
