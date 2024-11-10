require('dotenv').config();
const request = require('request');
const compression = require('compression');
const cors = require('cors');
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);

const port = process.env.SERVER_PORT || 3000;
const telegramBotToken = process.env.TELEGRAM_BOT_TOKEN;

app.use(express.static('dist', {index: 'demo.html', maxage: '4h'}));
app.use(compression());
app.use(bodyParser.json());

// handle admin Telegram messages
app.post('/hook', function(req, res){
    try {
        const message = req.body.message || req.body.channel_post;
        const chatId = message.chat.id;
        const name = message.chat.first_name || message.chat.title || "admin";
        const text = message.text || "";
        const reply = message.reply_to_message;

        if (text.startsWith("/start")) {
            console.log("/start chatId " + chatId);
            sendTelegramMessage(chatId,
                "*Welcome to Intergram* \n" +
                "Your unique chat id is `" + chatId + "`\n" +
                "Use it to link between the embedded chat and this telegram chat");
        } else if (reply) {
            let replyText = reply.text || "";
            let userId = replyText.split(':')[0];
            io.emit(chatId + "-" + userId, {name, text, from: 'admin'});
        } else if (text){
            io.emit(chatId, {name, text, from: 'admin'});
        }

    } catch (e) {
        console.error(e);
    }
    res.sendStatus(200);
});

http.listen(port, function(){
    console.log('listening on *:' + port);
});

function sendTelegramMessage(chatId, text) {
    const url = `https://api.telegram.org/bot${telegramBotToken}/sendMessage`;
    request.post(url, {
        json: {
            chat_id: chatId,
            text: text,
            parse_mode: 'Markdown'
        }
    });
}
