import os
from collections import defaultdict


def generate_html(folder_path):
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Material Icons Filter</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                margin: 0;
            }
            nav {
                width: 200px;
                padding: 20px;
                border-right: 1px solid #ccc;
                position: fixed;
                height: 100vh;
                overflow-y: auto;
                background-color: #f8f8f8;
            }
            nav ul {
                list-style-type: none;
                padding: 0;
            }
            nav li {
                margin-bottom: 10px;
            }
            nav a {
                text-decoration: none;
                color: #007BFF;
            }
            nav a:hover {
                text-decoration: underline;
            }
            .content {
                flex-grow: 1;
                padding: 20px;
                margin-left: 240px;
            }
            .genre {
                margin-bottom: 50px;
            }
            h2 {
                margin-top: 50px;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
                gap: 10px;
            }
            .grid img {
                width: 100%;
                height: auto;
                border: 1px solid #ccc;
                cursor: pointer;
            }
            .grid img.selected {
                border-color: #FF0000;
            }
            .output-btn {
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #007BFF;
                color: #fff;
                text-align: center;
                cursor: pointer;
            }
            .select-all-btn {
                margin: 10px 0;
                padding: 5px 10px;
                background-color: #28A745;
                color: #fff;
                cursor: pointer;
                display: inline-block;
            }
        </style>
    </head>
    <body>
        <nav>
            <h1>Material Icons Filter</h1>
            <ul>
    """

    genre_dict = defaultdict(list)

    # genre/name 階層を探索して、materialicons/24px.svg を取得する
    for root, dirs, files in os.walk(folder_path):
        if 'materialicons' in dirs:
            # genre (親ジャンル) と name (子ジャンル) を分けて取得
            genre_path = os.path.relpath(root, folder_path)
            genre = genre_path.split(os.sep)[0]  # genre部分だけを取得
            svg_path = os.path.join(root, 'materialicons', '24px.svg')
            if os.path.exists(svg_path):
                genre_dict[genre].append(svg_path)

    # ナビゲーションメニューを生成
    for genre in genre_dict:
        genre_id = genre.replace('/', '_').replace(' ', '_')
        html_content += f'<li><a href="#{genre_id}">{genre}</a></li>\n'

    html_content += """
            </ul>
            <div class="output-btn" onclick="outputSelection()">選択を出力</div>
        </nav>
        <div class="content">
    """

    # 親ジャンルごとのコンテンツを生成
    for genre, files in genre_dict.items():
        genre_id = genre.replace('/', '_').replace(' ', '_')
        html_content += f'<div class="genre" id="{genre_id}">\n<h2>{genre}</h2>\n'
        html_content += f'<div class="select-all-btn" onclick="toggleGenreSelection(\'{genre_id}\')">全て選択</div>\n'
        html_content += f'<div class="grid">\n'
        for file in files:
            relative_path = os.path.relpath(file, folder_path)
            html_content += f'<img src="{relative_path}" alt="{relative_path}" onclick="toggleSelection(this)">\n'
        html_content += '</div>\n</div>\n'

    # HTMLを閉じる
    html_content += """
        </div>

        <script>
            const selectedItems = [];

            function toggleSelection(img) {
                const index = selectedItems.indexOf(img.alt);
                if (index > -1) {
                    selectedItems.splice(index, 1);
                    img.classList.remove('selected');
                } else {
                    selectedItems.push(img.alt);
                    img.classList.add('selected');
                }
            }

            function toggleGenreSelection(genreId) {
                const genreDiv = document.getElementById(genreId);
                const images = genreDiv.querySelectorAll('img');
                let allSelected = true;

                images.forEach(img => {
                    if (!img.classList.contains('selected')) {
                        allSelected = false;
                    }
                });

                images.forEach(img => {
                    if (allSelected) {
                        selectedItems.splice(selectedItems.indexOf(img.alt), 1);
                        img.classList.remove('selected');
                    } else {
                        if (!img.classList.contains('selected')) {
                            selectedItems.push(img.alt);
                            img.classList.add('selected');
                        }
                    }
                });
            }

            function outputSelection() {
                const output = JSON.stringify(selectedItems, null, 2);
                const outputWindow = window.open('', '_blank');
                outputWindow.document.write('<pre>' + output + '</pre>');
                outputWindow.document.close();
            }
        </script>
    </body>
    </html>
    """

    # HTMLファイルに書き込む
    output_file = os.path.join(folder_path, 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"カタログページが {output_file} に生成されました！")


# 使用例
generate_html('./')  # フォルダのパスをここに入れてね
