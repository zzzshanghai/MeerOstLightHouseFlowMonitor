腾讯云轻量应用服务器流量告警

基于https://github.com/2lifetop/LightHouse_Automatic_Shutdown 二改

教程：
## 情景引入

> 众所周知，作为“良心云”的腾讯云很早之前就推出了`轻量应用服务器`，其中最受青睐的就是香港轻量应用服务器了，作为一枚穷人，博主也是用的1H2G的香港轻量。虽然性价比高，但也有无奈的一面，如：每月流量限制，超出另计费。作为白嫖党，自然不能因为DDOS而让自己走上破产。所以我借助 <a href="https://github.com/2lifetop/LightHouse_Automatic_Shutdown/" target="_blank" rel="nofollow">2lifetop</a> 提供的源代码，实现了实时流量监控以及超出流量限制自动关机。

## 设置ID和KEY

> 由于项目需要腾讯云服务器的实时数据和钉钉机器人。
>
> 所以需要设置腾讯云的`SecretId`和`SecretKey`，以及钉钉机器人的`Token`。

### 获取腾讯云API密钥

前往 <a href="https://console.cloud.tencent.com/cam/capi" target="_blank" rel="nofollow">访问密钥 - 控制台</a> ，点击新建 密钥，复制获取的`SecretId`和`SecretKey`，等一会儿会用到。

![腾讯云API](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122140610.JPG)

### 获取钉钉机器人Token

打开电脑端的钉钉，新建一个群，打开群设置，点击智能群助手下的添加机器人，

![钉钉机器人](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122153576.JPG)

再选择自定义机器人，

![钉钉机器人](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122311879.JPG)

再根据图示：

![钉钉机器人](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122155892.JPG)

先填写机器人名称，再将安全设置的自定义关键词打勾，填写关键词为“流量告警”。

最后找到“4”中的`Token`，其链接形式如`https://oapi.dingtalk.com/robot/send?access_token=973e7b241234567890141d60c24e9e71234567890d7a4cef18ed9ec2fedfvfd`

只需记录`token`后面的值，即`973e7b241234567890141d60c24e9e71234567890d7a4cef18ed9ec2fedfvfd`

## `Github Fork`项目，设置相关数据

### `Fork`项目

前往 <a href="https://github.com/MeerOst/MeerOstLightHouseFlowMonitor" target="_blank">腾讯云轻量应用服务器流量告警</a> 点击右上角的`Fork`按钮。

### 相关配置

#### ID和Key设置

打开你的流量监控的项目仓库，并找到仓库设置，选择Secrets，再点击`New repository secret`按钮新建`Secret`

![Github](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122213998.JPG)

然后像这样填写相关数据：

![Github](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122213647.JPG)

 其中四个相关值的填写格式如下：

```yaml
- SecretId
 name: SecretId
 value: AKIDe8NL2TeABCDEABCDE8AxTigNnyt12345 
- SecretKey
 name: SecretKey
 value: NUKvFI4dy2pMdePu812345wdoasebcde
- 钉钉机器人token
 name: webhook
 value: "973e7b241234567890141d60c24e9e71234567890d71234518ed9ec2fe123456" #注意添加双引号
```

#### 修改配置

##### 更改运行频率：

这可以通过修改`.github/workflows/LH.yml`中`schedule`的`cron`参数来达到目的，

如我的，每5分钟运行一次就是：

```yml
  schedule:
    - cron: "*/5 * * * *"
```

如果需要修改成其他的频率，请参考[2lifetop](https://2demo.top/231.html)提供的教程。

##### 关机百分比

此举的目的是，如果服务器的流量达到你设定的百分比，就自行关机，可以根据实际情况更改。

如图：你需要修改这个`LH.py`中的`percent`值

![Github](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122232807.JPG)

## 运行项目

根据如图的顺序即可运行配置

![Github](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122237405.JPG)

你也可以点击运行的项目查看运行结果

> 效果展示：
>
> ### `github`
>
> ![Github](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122248062.JPG)
>
> ### 钉钉
>
> ![钉钉机器人](https://gitee.com/MeerOst/MeerOstDrawingBed/raw/master/RaumzeitBlog/202108122251320.JPG)

> 

> 这其中也有TG酱 ，可以通知关机信息，由于其需要科学上网，所以我并没有设置

> 你可以去`telegram`搜索 <a href="https://t.me/realtgchat_bot" target="_blank" rel="nofollow">@realtgchat_bot</a>，获取`token`

> 其在`Secrets`的数据填写形式如下：

```yaml
- TG酱
 name: tgToken
 value: "WnU3abcdREYxNjQ5NzA12345" #注意双引号
```

> 最后，由衷感谢 <a href="https://github.com/2lifetop/LightHouse_Automatic_Shutdown/" target="_blank" rel="nofollow">2lifetop </a> 提供的源码。
