腾讯云轻量应用服务器流量告警

基于https://github.com/2lifetop/LightHouse_Automatic_Shutdown 二改

教程：
# Hexo主题Aurora的魔改（一）

刚接触`Hexo`，就碰到了这么好的主题，如图是`Aurora`作者的博客展示：

你可以从去<a href="https://github.com/auroral-ui/hexo-theme-aurora" target="_blank" rel="nofollow">Github</a>了解`Hexo`和`Aurora`主题。

![Aurora主题展示](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108111419889.png)

虽然主题很好看，但是对于刚接触`Hexo`，折腾起来是有点棘手。

安装出现问题，主题修改摸不着头脑，`Deploy`出现问题。

下面我将从替换源站静态文件和图片文件链接，以及替换`cdnjs.cloudflare.com`链接两个方面来介绍我修改的内容，以后可能还有，敬请期待。

## 替换源站链接

由于`github.io`在国内的访问速度很慢，而且也不容易被爬虫抓取，所以我果断选择了在自己的服务器上部署hexo发布的静态文件，关于 如何通过宝塔在自己的服务器上部署`hexo`站点，可以参考 这两位 博主的做法 :

<a href="https://www.heson10.com/posts/51315.html" target="_blank" rel="nofollow">Hexo 部署至云服务器（宝塔面板） - 黑石博客 - Hexo博客 (heson10.com)</a>

<a href="https://www.jsopy.com/2020/03/08/setuphexo/" target="_blank" rel="nofollow">用宝塔面板将hexo部署到阿里云 | JSOPY</a>

如果` Hexo d `时碰到 `bash: git-receive-pack: command not found fatal: Could not read from remote repository. `这样的问题，可以参考：

<a href="https://blog.csdn.net/li1325169021/article/details/111874334" target="_blank" rel="nofollow">bash: git-receive-pack: command not found fatal: Could not read from remote repository._小志的博客-CSDN博客</a>

但是问题又来了，由于我是用的腾讯云的1H2G的香港轻量，资源不够，所以想像`wordpress`那样弄一个CDN，以及自动替换源站链接为CDN链接，但是搜索了一圈，也没能找到好的方法来自动替换链接，以下是我搜索到的方法，都不太有用，如果有网友实验成功，可以告知以下博主，我也想白嫖。

<a href="https://renzibei.com/2020/07/12/使用jsdelivr-CDN-加速hexo的图片等静态资源加载/" target="_blank" rel="nofollow">自动使用jsdelivr CDN 加速hexo的图片等静态资源加载 | 鸿雁自南人自北 (renzibei.com)</a>

<a href="https://segmentfault.com/a/1190000022531769" target="_blank" rel="nofollow">使用 jsDelivr 免费加速 GitHub Pages 博客的静态资源 - SegmentFault 思否</a>

<a href="https://blog.yuanpei.me/posts/1417719502/" target="_blank" rel="nofollow">使用 jsDelivr 为 Hexo 博客提供高效免费的CDN加速 | 素履独行 (yuanpei.me)</a>

暂时没法，只能一个个去替换使用的链接，

### 1.替换head里的link

找到路径：`Hexo\node_modules\hexo-theme-aurora\layout\index.js`

修改head头里面的引用链接，如：

`/favicon.ico`

`/static/css/chunk-libs.eebac533.css`

`/static/css/app.0d31776f.css`

将这些链接修改为你的cdn链接，如`jsdelivr`

### 2.其他链接替换

还是上面的`index.ejs`文件，ctrl+f搜索  ` i.p="/"   `

将  ` i.p="/" `  改为cdn链接 ，如：`i.p="https://cdn.jsdelivr.net/gh/MeerOst/meerost.github.io@master/"`

这样即可，去游览器f12，可以看到源站链接只有html和json文件了

## 替换`cdnjs.cloudflare.com`链接

由于主题引用了`cdnjs.cloudflare.com`链接，而这个域名在国内访问慢，ping值高，所以速度并不理想，甚至还会出现一直绕圈的情况。所以需要替换链接，

f12查看，原来是由于引用了`clipboard.min.js`文件，而这个文件的引用链接并没有出现在主题文件里面，说明是引用的外部文件里面包含了这个`clipboard.min.js`文件的引用链接，查与`clipboard`相关的外部文件，发现是`prism-copy-to-clipboard.min.js`文件，引用了`clipboard.min.js`文件，现在只需修改`prism-copy-to-clipboard.min.js`引用链接就可以了。

这里有许多方法，你可以自己琢磨一下，我的方法是，

### 1.下载`clipboard.min.js`文件

下载`clipboard.min.js`文件，并上传到github上，找到其jsdelivr的cdn链接

，如：`https://cdn.jsdelivr.net/gh/MeerOst/MeerOstPubilcStatic/ajax/libs/clipboard.js/2.0.0/clipboard.min.js`

### 1.下载`prism-copy-to-clipboard.min.js`

下载`prism-copy-to-clipboard.min.js`文件，将`https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.0/clipboard.min.js`链接替换为jsdelivr的cdn链接，最后将`prism-copy-to-clipboard.min.js`文件上传到`github`，并找到其`jsdelivr`的cdn链接，如：`https://cdn.jsdelivr.net/gh/MeerOst/MeerOstPubilcStatic/npm/prismjs@1.23.0/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js`

### 3.替换本地文件链接

找到本地路径：`Hexo\\node_modules\hexo-theme-aurora\data\en.yml` 打开`en.yml`文件，或`Hexo\\node_modules\hexo-theme-aurora\data\en.yml`的`cn.yml`文件（看你`_config.aurora.yml`里面的cdn配置使用的是cn还是en）将`prism-copy-to-clipboard.min.js`文件的引用链接替换为上面的`jsdelivr`的cdn链接。

:::tip Valine评论无法显示问题

​	- 如果你在cdn配置为en时，valine会出现无法显示的情况（cn我不知道会不会也有这种情况）

​	- 最后查明是`Valine.min.js`文件报错：不存在，你需要找到

​	- `Hexo\node_modules\hexo-theme-aurora\data\en.yml `

​	- 文件，将其中`Valine.min.js`的引用链接改为

​	- `https://cdn.jsdelivr.net/`

​	- `npm/valine@1.4.14/dist/`

​	- `Valine.min.js`(请自行需要将链接拼接)。

:::
