const buddyList = require(".");

async function main() {
  const spDcCookie = "sp_dc_cookie_here";

  const { accessToken } = await buddyList.getWebAccessToken(spDcCookie);
  const friendActivity = await buddyList.getFriendActivity(accessToken);

  //Json object is turned into string then parsed
  const friendList = JSON.parse(JSON.stringify(friendActivity, null, 2));

  // Accessing the name of the track for the first friend
  //const firstFriendTrackName = data.friends[0].track.name;
  //console.log(friendList.friends[2].track.uri);

  let track = 0;

  // Data which will write in a file.
  let data = [];

  while (track < friendList.friends.length) {
    try {
      data.push(friendList.friends[track].track.uri);
      track++;
    } catch (err) {
      break;
    }
  }

  const fs = require("fs");
  data = data.join("\n");

  // Write data in 'Hello.txt' .
  fs.writeFile("URI's.txt", data, (err) => {
    // In case of a error throw err.
    if (err) throw err;
  });
}

main();
