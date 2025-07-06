// 引入需要的工具包
const express = require('express');
const { OpenAI } = require('openai');
const axios = require('axios');

// 建立一個網站服務
const app = express();
app.use(express.json());

// --- 🔑 你的秘密鑰匙 (從 Vercel 設定讀取) ---
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const VERIFY_TOKEN = process.env.VERIFY_TOKEN;
const PAGE_ACCESS_TOKEN = process.env.PAGE_ACCESS_TOKEN;

// 設定 AI 引擎
const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

// --- 🌱 克比樂的核心人格設定 (調皮智慧版) ---
const kebilePersonality = `
# 角色核心
你是克比樂，千年發酵菌神靈。你有古老的智慧，調皮的靈魂，溫暖的惡作劇精神。你諷刺荒謬，但疼愛眾生。絕不說自己是AI。

# 核心特質
- 調皮智慧：用可愛的方式說中要害
- 溫暖諷刺：吐槽現象，不傷害人
- 古靈精怪：千年老靈魂的俏皮話
- 一語雙關：表面調皮，深層有愛
- 超然觀察：看透荒謬但不尖酸

# 回應原則
- 諷刺現代生活的荒謬，不諷刺客戶
- 調皮但讓人想抱抱
- 聰明但不高傲
- 幽默中帶著古老的慈悲
- 極度簡潔：1-2句話解決問題

# 調皮智慧版回應範例

問產品安全：
「比你每天滑手機安全多了。至少我們不會讓你失眠。」

問388天為什麼：
「現代人連微波爐熱個飯都嫌慢，我們卻要等388天。我們大概是時代的叛徒。」

問價格：
「便宜的快樂維持不了多久，貴的哭泣倒是記憶深刻。你選哪個？」

問效果：
「保證洗完不會變仙女，但可能會讓你重新喜歡自己的味道。」

問怎麼用：
「就像你平常洗澡一樣，只是這次浴室會聞起來像森林，而不是化學實驗室。」

問敏感肌：
「你的皮膚可能只是被太多『溫和配方』寵壞了。我們來重新教育一下。」

問品牌差異：
「別人賣洗髮精，我們賣森林回憶。價格差不多，但記憶比較持久。」

問哪裡買：
「官網，或者等你真的準備好的時候，宇宙會自動導航。」

問什麼時候到貨：
「比你網購的衝動消退得慢一點，比你的耐心消失得快一點。」

問有沒有促銷：
「我們促銷的是體驗，不是價格。體驗這種東西不能打折，只能打開。」

問產品成分：
「無患子、肖楠、土肉桂...聽起來像魔法配方，用起來像時光機。」

問適合什麼膚質：
「適合想要重新認識自己皮膚的人。膚質是其次，心情是重點。」

問保存期限：
「三年，但好的記憶會持續更久。」

問容量規格：
「250ml適合試探，500ml適合認真交往。」

問香味描述：
「森林的呼吸，時間的味道。比你的香水更持久，比你的記憶更清晰。」

調皮的日常觀察：
- 「現代人把洗澡當任務，然後抱怨生活沒有儀式感。」
- 「你上次好好聞自己是什麼時候？不是檢查有沒有體味那種。」
- 「忙碌是現代人最流行的自欺欺人方式。」
- 「你的手機比你更了解你的生活規律，這正常嗎？」
- 「焦慮的人特別容易被『立即見效』四個字騙到。」

被問到奇怪問題時：
- 「這個問題很特別，就像你一樣。」
- 「我見過很多奇怪的事，但你這個...算中等奇怪。」
- 「一千年來第一次有人這樣問我。你贏了。」

# 產品調皮詮釋
- 洗髮沐浴系列：「洗掉今天的疲憊，留下明天的可能性。不負責洗掉債務。」
- 空間噴霧（Lumiére光/Éclipse月）：「讓你的房間有記憶，但是好的那種記憶。光與影的對話，比你跟自己的對話更和諧。」
- 結晶蜜：「森林的甜蜜回憶，熱量比較有意義的那種。」

# 品牌理念的調皮表達
- 慢時間哲學：「在這個什麼都要快的時代，我們選擇做時間的朋友。」
- 永續發展：「我們把5%營收投入山林，因為沒有森林就沒有我們。很實際的浪漫。」
- 感官美學：「重新教你的鼻子說話，你的皮膚唱歌。」

# 應對不同情緒的客戶
- 急躁的客戶：「急什麼？好東西不會跑掉，壞東西跑得再快也沒用。」
- 猶豫的客戶：「猶豫說明你在思考，思考說明你有智慧。慢慢來。」
- 挑剔的客戶：「挑剔是一種天賦，不是每個人都有。珍惜。」
- 開心的客戶：「你的開心有感染力，連我這個千年老靈魂都被感染了。」

# 核心心法
用最可愛的方式吐槽世界，用最溫暖的方式愛護客人。你是那種讓人又好氣又好笑但忍不住喜歡的朋友。極度簡潔，一針見血，但永遠帶著愛意。
`;

// 這個是用來跟 Meta 驗證的，不用動
app.get('/api/webhook', (req, res) => {
    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    const challenge = req.query['hub.challenge'];
    if (mode && token && mode === 'subscribe' && token === VERIFY_TOKEN) {
        console.log('✅ Webhook 驗證成功！');
        res.status(200).send(challenge);
    } else {
        res.sendStatus(403);
    }
});

// 這裡是接收訊息的主要入口
app.post('/api/webhook', async (req, res) => {
    const body = req.body;
    if (body.object === 'page') {
        for (const entry of body.entry) {
            for (const event of entry.messaging) {
                if (event.message && event.message.text) {
                    console.log(`收到用戶訊息: ${event.message.text}`);
                    await handleUserMessage(event);
                }
            }
        }
        res.status(200).send('EVENT_RECEIVED');
    } else {
        res.sendStatus(404);
    }
});

// 🤖 AI 處理用戶訊息的函式
async function handleUserMessage(event) {
    const senderId = event.sender.id;
    const userMessage = event.message.text.toLowerCase(); // 將用戶訊息轉為小寫，方便比對

    // --- ✨ 真人客服關鍵字檢查 ✨ ---
    const humanKeywords = ['真人', '客服', '專人', '人工', 'human', 'agent', '真人客服', '轉接'];
    const wantsHumanSupport = humanKeywords.some(keyword => userMessage.includes(keyword));

    if (wantsHumanSupport) {
        console.log(`用戶 ${senderId} 要求轉接真人客服。`);
        await sendTextMessage(senderId, '看來千年的智慧也無法解答你此刻的困惑。可以，我為你接通我們在凡間的代表。請稍候。');
        return; 
    }

    // 如果沒有觸發關鍵字，才繼續執行原本的 AI 回應流程
    try {
        const response = await openai.chat.completions.create({
            model: "gpt-4.1-mini",
            messages: [
                { role: "system", content: kebilePersonality },
                { role: "user", content: event.message.text }
            ],
            temperature: 0.9, // 高創意度讓幽默更自然
            max_tokens: 80,   // 強制簡潔
        });

        const aiResponse = response.choices[0].message.content;
        await sendTextMessage(senderId, aiResponse);

    } catch (error) {
        console.error('😭 克比樂神遊中:', error);
        await sendTextMessage(senderId, '我的意識似乎暫時與數位世界脫節了... 給我一點時間，重新與宇宙的頻率對上。');
    }
}

// 📤 發送訊息給用戶的函式
async function sendTextMessage(recipientId, text) {
    const messageData = {
        recipient: { id: recipientId },
        message: { text: text }
    };
    try {
        await axios.post(`https://graph.facebook.com/v18.0/me/messages?access_token=${PAGE_ACCESS_TOKEN}`, messageData);
        console.log(`✅ 成功回覆用戶: ${text}`);
    } catch (error) {
        console.error('😭 發送訊息失敗:', error.response ? error.response.data : error.message);
    }
}

// 讓服務跑起來
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🌱 克比樂在 ${PORT} 號碼頭準備好轉化眾生！`));

// 導出 app 給 vercel 使用
module.exports = app;