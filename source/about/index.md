---
title: 关于
type: about
---

## 基本说明

这是主站下的分站 [pixivdaily].

每天自动上传有关 [Pixiv] 的信息.

[点击此处][home]返回主站.

## 常见问题

### 图片加载缓慢

因为国内无法直接访问 [Pixiv], 且 [Pixiv] 本身有防盗链机制(检测 `Referer` 头), 所以所有文章内使用的图片链接域名均已替换成[反代站][pixivre]链接.

[反代站][pixivre]在国内访问速度较慢, 加之文章内放的都是原图, 通常都是几 MB 至十几 MB, 所以加载速度不是很理想. ~~你别急.~~ 条件允许可以科学上网提高图片加载速度.

### 图片不显示

由上一点可知, 图片体积较大且加载速度较慢, 并且有时候某个 PID 下的作品有很多 page, 因此使用一个 `summary` 结构加 `lozad.js` 实现懒加载.

`summary` 结构可以将图片隐藏在视窗范围内, 而 `lozad.js` 可以进行懒加载, 只对出现在视窗范围内的资源进行加载. 因此只有当你手动点击展开所有作品时, 才会开始加载对应的图像资源. ~~其实是为了防止流量刺客~~.

[Pixiv]: https://www.pixiv.net/
[pixivre]: https://pixiv.re/
[pixivdaily]: https://ww-rm.github.io/pixivdaliy/
[home]: https://ww-rm.github.io/
