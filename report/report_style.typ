// Chinese localization of the unmodified modern-g7-32 0.2.0 template.
#import "template/modern-g7-32/export.typ": gost
#import "template/modern-g7-32/component/title-templates.typ": templates

#let report(body) = [
#show: gost.with(
  title-template: templates.default,
  text-size: (default: 11pt, small: 9pt),
  margin: (left: 22mm, right: 22mm, top: 22mm, bottom: 20mm),
  indent: 0pt,
  ministry: none,
  organization: (full: none, short: none),
  about: none,
  report-type: none,
  research: none,
  subject: none,
  federal: none,
  city: none,
  year: none,
  add-pagebreaks: false,
  hide-title: true,
  performers: none,
  manager: (position: none, name: none, title: none),
)

#set document(title: "基于 ZYNQ-7020 的低延迟固定目标人物人声转换系统设计报告", author: "Pi-debug-cmd contributors")
#set text(font: ("Times New Roman", "SimSun"), lang: "zh", hyphenate: false)
#set par(justify: true, first-line-indent: 0pt, leading: 0.6em, spacing: 0.8em)
#set page(footer: context {
  if counter(page).get().first() > 1 {
    align(center, text(size: 9pt)[第 #counter(page).display() 页])
  }
})

#set par(justify: false, first-line-indent: 0pt, leading: 0.5em, spacing: 0pt)
#v(10mm)
#align(center)[#text(size: 13pt, fill: rgb("4c7f88"), weight: "semibold")[全国大学生嵌入式芯片与系统设计竞赛 2026]]
#v(18mm)
#align(center)[
  #text(size: 21pt, font: "Microsoft YaHei", fill: rgb("203746"), weight: "medium")[基于 ZYNQ-7020 的低延迟]
  #linebreak()
  #text(size: 21pt, font: "Microsoft YaHei", fill: rgb("203746"), weight: "medium")[固定目标人物人声转换系统设计报告]
]
#v(13mm)
#align(center)[#text(size: 13pt, fill: rgb("6f7f86"))[全国大学生嵌入式芯片与系统设计竞赛 AMD 自主选题初级组]]
#v(14mm)
#align(center)[#rect(width: 65%, height: 2.5pt, fill: rgb("4c7f88"))]
#v(14mm)
#set text(size: 10.5pt, fill: rgb("253746"))
#table(
  columns: (1.15fr, 3.85fr),
  align: left + horizon,
  stroke: 0.5pt + rgb("bcc7cc"),
  inset: (x: 10pt, y: 10pt),
  fill: (x, y) => if x == 0 { rgb("eaf0f1") } else { white },
  [#text(weight: "bold")[目标平台]], [野火 Zynq-7020，xc7z020clg400-2],
  [#text(weight: "bold")[软硬件划分]], [ARM Cortex-A9 PS + Vitis HLS PL + Linux coherent-DMA],
  [#text(weight: "bold")[项目版本]], [Round30 持久启动候选；来源版本 PL-20261027-01],
  [#text(weight: "bold")[报告日期]], [2026 年 11 月 3 日],
)
#v(1fr)
#text(size: 10pt, weight: "semibold", fill: rgb("203746"))[报告范围]
#v(3mm)
#set par(justify: true, first-line-indent: 0pt, leading: 0.5em, spacing: 0pt)
#text(size: 10pt, fill: rgb("53636c"))[本报告介绍 WORLD 实时语音流程中的 PS/PL 协作实现：PS 承担音频采集、WORLD 主流程与调度，PL 执行选定的 1024 点最小相位频谱计算，并汇总项目设计、接口、实验结果、技能沉淀和复现流程。]
#pagebreak()

#set par(justify: true, first-line-indent: 0pt, leading: 0.6em, spacing: 0.8em)
#set heading(numbering: none)
#show heading: set text(font: ("Arial", "SimHei"))
#show heading: set block(above: 1.2em, below: 0.7em)
#show heading.where(level: 1): set text(size: 14pt)
#show heading.where(level: 2): set text(size: 11.5pt)
#set list(marker: [•], indent: 0pt, body-indent: 1em, spacing: 0.4em)
#set enum(indent: 0pt, body-indent: 1.5em, spacing: 0.5em)
#show raw: set text(font: ("Consolas", "SimSun"), size: 0.88em)
#show raw.where(block: true): it => block(width: 100%, fill: rgb("f4f5f6"), inset: 9pt, radius: 0pt)[
  #set par(justify: false, first-line-indent: 0pt, leading: 0.4em)
  #it
]
#set figure(supplement: [图])
#show figure.where(kind: image): set figure(supplement: [图])
#set figure.caption(separator: "  ")
#show figure.caption: set text(size: 9.5pt)
#set page(footer: context {
  if counter(page).get().first() == 1 {
    align(center)[2026 年 11 月 3 日]
  } else {
    align(center, text(size: 9pt)[第 #counter(page).display() 页])
  }
})

#body
]

// All five tables share cell alignment, font, padding, and page-break rules.
#let report-table(columns, caption, rows) = {
  set par(justify: false, first-line-indent: 0pt, leading: 0.45em, spacing: 0pt)
  set text(size: 9.5pt)
  show table.cell: set align(left)
  set figure(supplement: [表])
  block(breakable: false, figure(
    block(breakable: false, width: 100%)[
      #table(
        columns: columns,
        align: left + top,
        stroke: 0.45pt + rgb("a6b1bd"),
        inset: (x: 6pt, y: 6pt),
        fill: (x, y) => if y == 0 { rgb("edf1f5") } else { white },
        table.header(..rows.first().map(cell => strong(cell))),
        ..rows.slice(1).flatten(),
      )
    ],
    kind: table,
    caption: caption,
    placement: none,
  ))
}

// Permit line wrapping in long source paths and commit identifiers.
#let code(value) = {
  let body = if value.match(regex("^[0-9a-f]{40}$")) != none {
    text(value.slice(0, 20)) + linebreak() + text(value.slice(20))
  } else {
    value.clusters().map(char => {
      text(char) + if char in ("/", "_", "-", " ") { sym.zws } else { [] }
    }).join()
  }
  text(font: ("Consolas", "SimSun"), size: 0.88em, body)
}
