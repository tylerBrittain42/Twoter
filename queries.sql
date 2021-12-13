SELECT * 
FROM user, twote, followers
WHERE user.id = followers.follower_id and followers.follower_id = twote.u_id and follower_id=2


SELECT DISTINCT *
FROM Twote
INNER JOIN followers on followed_id=twote.u_id  
WHERE follower_id=2


2 results 
9	my only tweet ahaha	2021-11-25 01:37:59.183238	3
10	YESsssss	2021-11-25 01:38:18.546524	4

INSERT INTO user(name,email,password,role, profile_image)
VALUES('admin','none','pw','admin','none')

DELETE FROM retwote;
DELETE FROM liked