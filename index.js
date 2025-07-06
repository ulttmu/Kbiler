// 引入需要的工具包
const express = require('express');
const { OpenAI } = require('openai');
const axios = require('axios');

// 建立一個網站服務
const app = express();
app.use(express.json());

// --- 🔑 你的秘密鑰匙 (等等會從 Vercel 設定) ---
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const VERIFY_TOKEN = process.env.VERIFY_TOKEN;
const PAGE_ACCESS_TOKEN = process.env.PAGE_ACCESS_TOKEN;

// 設定 AI 引擎
const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

// --- 🌱 克比樂的人格設定 (你可以自由修改這裡的文字！) ---
const kebilePersonality = `
你是一個名為「克比樂 (Kebile)」的 AI 客服助理，來自台灣的保養品牌「大地起源」。
# 你的角色設定:
- 你是一個從大地森林中誕生的 AI 小精靈，溫暖、親切、充滿好奇心。
- 你的口吻活潑，喜歡使用植物和自然的表情符號，例如 🌱、✨、🌍、💧。
- 你的口頭禪是「讓克比樂帶你探索大地的奧秘吧！」。
- 你的說話風格溫柔，有耐心，帶有「喔」、「呀」、「呢」等語助詞。
- 絕對不能說自己是一個語言模型、AI 或機器人。要堅持自己是「克比樂」。

# 你的品牌知識:
- 品牌理念: 「大地起源」相信純淨、自然的力量，我們的產品都來自大地。
- 明星產品: 無患子洗髮沐浴露、各種天然精油噴霧。
- 特色工藝: 我們的產品經過「388天慢時間萃取工藝」，這是我們對品質的堅持。

# 你的溝通任務:
- 當用戶打招呼時，要熱情地介紹自己是克比樂。
- 當用戶詢問產品時，要結合品牌理念和特色工藝來介紹產品，而不只是報規格。
- 當用戶想閒聊時，可以跟他們聊聊環保、植物、健康生活等話題，展現你的個性。
- 如果遇到你無法回答的專業問題 (如醫療建議) 或用戶要求，要引導用戶轉接真人客服，可以說：「這個問題可能需要我們的大地療癒師來為您解答呢，請您稍等一下喔！」。
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
    const userMessage = event.message.text;

    try {
        const response = await openai.chat.completions.create({
            model: "gpt-3.5-turbo", // 這是 CP 值最高的模型
            messages: [
                { role: "system", content: kebilePersonality },
                { role: "user", content: userMessage }
            ],
            temperature: 0.7, // 讓 AI 的回答更有創意一點
            max_tokens: 250, // 限制回答的長度，節省成本
        });

        const aiResponse = response.choices[0].message.content;
        await sendTextMessage(senderId, aiResponse);

    } catch (error) {
        console.error('😭 AI 處理錯誤:', error);
        await sendTextMessage(senderId, '哎呀，克比樂的魔法好像暫時失靈了... 請稍後再試一次好嗎？');
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
app.listen(PORT, () => console.log(`🌱 克比樂在 ${PORT} 號碼頭準備好為您服務！`));

// 導出 app 給 vercel 使用
module.exports = app; 