// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    const sidebarList = document.getElementById('sidebar-list');
    const displayArea = document.getElementById('article-display');

    // 1. 記事一覧をAPIから取得してサイドバーに表示
    function fetchArticles() {
        fetch('/api/articles')
            .then(response => response.json())
            .then(articles => {
                sidebarList.innerHTML = ''; // 一旦クリア
                articles.forEach(article => {
                    const div = document.createElement('div');
                    div.className = 'article-item';
                    div.innerHTML = `
                        <span class="item-title">${article.title}</span>
                        <span class="item-date">${article.date}</span>
                    `;
                    // クリックしたら詳細を表示
                    div.onclick = () => loadArticleDetail(article.id, div);
                    sidebarList.appendChild(div);
                });
            })
            .catch(error => console.error('Error fetching articles:', error));
    }

    // 2. 記事の詳細を取得してメインエリアに表示
    function loadArticleDetail(id, element) {
        // アクティブな項目の見た目を変える
        document.querySelectorAll('.article-item').forEach(el => el.classList.remove('active'));
        element.classList.add('active');

        fetch(`/api/articles/${id}`)
            .then(response => response.json())
            .then(data => {
                displayArea.innerHTML = `
                    <h1>${data.title}</h1>
                    <div class="article-meta">著者: ${data.author} | 日付: ${data.date}</div>
                    <div class="article-body">
                        ${data.content.replace(/\n/g, '<br>')} 
                    </div>
                `;
            })
            .catch(error => console.error('Error loading article details:', error));
    }

    // 初期読み込み
    fetchArticles();
});