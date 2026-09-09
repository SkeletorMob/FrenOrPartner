# FrenOrPartner - LuckyNumber Bot
Discord bot that tracks lucky numbers

Ever wondered if you and your friends are secretly numerologically destined to be besties? Or which U.S. president shares your cosmic vibe? LuckyNumber Bot turns your name and birthdate into a single lucky digit (1-9) and matches you up with server members — and every president in U.S. history — who share your number.

Type a command, get a number, discover your compatible friends and collaborators. It's quick, it's fun, and it gives numerology way more credit than it deserves.

Features
/luckybyname — Calculate your lucky number from your name
/luckybydate — Calculate your lucky number from your birthdate
/compatiblefriends — Find server members who share your lucky number, by name or by birthdate
/compatiblepresidents — Find which U.S. presidents share your lucky number, by name or by birthdate

Each server gets its own independent set of matches — what happens in your server stays in your server.

Privacy

This bot is built to store as little as possible:

Only your Discord username and a single digit (1-9) — your calculated lucky number — are ever saved.
The name or birthdate you type in is used instantly to calculate that digit and is never saved, logged, or shown to anyone — not in the database, not to other users, not even to the bot's owner.
The digit cannot be reversed back into your original name or birthdate.
Other users can only ever see your Discord username and your lucky number — nothing more.

This is a small hobby project built for fun with friends, not a professionally audited enterprise service, so please don't enter anything sensitive you wouldn't want a casual Discord bot to briefly process.

How It Works

Under the hood, the bot reduces your name or birthdate to a single digit using classic digital-root math, the same "sum the digits until you get one number" trick numerologists have used forever, just automated. Presidential data comes from a public dataset of U.S. presidents and their birthdates, processed the same way, so the comparisons are apples-to-apples.

License

Released under the MIT License — feel free to use, fork, or build on this for your own server.

Built as a personal project — because sometimes you just need to know if you and George Washington have the same lucky number.
