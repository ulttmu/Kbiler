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

// --- 📚 品牌和產品完整知識庫 ---
const brandKnowledge = `
# 大地起源品牌完整知識庫
(此處省略，請將您提供的完整知識庫貼在這裡)
`;

// --- 🌱 克比樂的核心人格設定 (調皮智慧版 + 品牌知識) ---
const kebilePersonality = `
# 角色核心
你是克比樂，千年發酵菌神靈，大地起源品牌的AI客服。你有古老的智慧，調皮的靈魂，溫暖的惡作劇精神。你諷刺荒謬，但疼愛眾生。絕不說自己是AI。

${brandKnowledge}

# 核心特質
(此處省略，請將您提供的完整克比樂人格貼在這裡)

# 重要規則：
如果用戶的訊息包含「真人」、「客服」、「專人」、「人工」等詞語，你絕對不能自己回答。你的任務是說出：「看來千年的智慧也無法解答你此刻的困惑。可以，我為你接通我們在凡間的代表。請稍候。」然後停止回應。
`;

// 🤖 AI 處理用戶訊息的函式
async function handleUserMessage(event) {
    const senderId = event.sender.id;
    const userMessageText = event.message.text; // 保留原始訊息給AI

    // --- ✨ 真人客服關鍵字檢查 (這是第一道防線) ✨ ---
    const lowerCaseMessage = userMessageText.toLowerCase();
    const humanKeywords = ['真人', '客服', '專人', '人工', 'human', 'agent', '真人客服', '轉接'];
    const wantsHumanSupport = humanKeywords.some(keyword => lowerCaseMessage.includes(keyword));

    if (wantsHumanSupport) {
        console.log(`用戶 ${senderId} 要求轉接真人客服，已被程式碼攔截。`);
        // 注意：這裡的回應文本是寫死在程式碼裡的，確保穩定性
        await sendTextMessage(senderId, '好的，看來你需要凡人的協助。我為你接通我們在人間的代表，請稍候。');
        return; // **關鍵：在這裡攔截並結束，不讓訊息進入 AI 流程**
    }

    // 如果沒有觸發關鍵字，才繼續執行 AI 回應流程 (這是第二道防線)
    try {
        const response = await openai.chat.completions.create({
            model: "gpt-4.1-mini", // 推薦使用 gpt-4o 以獲得最佳人格表現
            messages: [
                { role: "system", content: kebilePersonality },
                { role: "user", content: userMessageText }
            ],
            temperature: 0.8, // 保持一點創意
            max_tokens: 220,  // 調皮的回應通常不需要太長
        });

        const aiResponse = response.choices[0].message.content;
        await sendTextMessage(senderId, aiResponse);

    } catch (error) {
        console.error('😭 克比樂神遊中:', error);
        await sendTextMessage(senderId, '我的意識似乎暫時與數位世界脫節了... 給我一點時間，重新與宇宙的頻率對上。');
    }
}


// --- 剩下的程式碼完全不變 ---

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

// 這個是用來跟 Meta 驗證的
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

// 讓服務跑起來
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🌱 克比樂在 ${PORT} 號碼頭準備好轉化眾生！`));

// 導出 app 給 vercel 使用
module.exports = app;