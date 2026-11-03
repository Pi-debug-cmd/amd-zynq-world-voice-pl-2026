// Chinese localization of the unmodified modern-g7-32 0.2.0 template.
#import "template/modern-g7-32/export.typ": gost
#import "template/modern-g7-32/component/title-templates.typ": templates

#let report(body) = [
#show: gost.with(
  title-template: templates.default,
  text-size: (default: 11pt, small: 9pt),
  margin: (left: 22mm, right: 22mm, top: 22mm, bottom: 20mm),
  indent: 0pt,
  ministry: [全国大学生嵌入式芯片与系统设计竞赛 2026],
  organization: (full: [AMD 自主选题初级组], short: none),
  about: none,
  report-type: text(size: 24pt, font: "SimHei")[技术设计报告],
  research: text(size: 19pt, font: "SimHei")[基于 Zynq-7020 的实时 WORLD 语音处理\ PS/PL 协同系统],
  subject: none,
  bare-subject: true,
  federal: [
    #v(12mm)
    #set text(size: 11pt)
    野火 Zynq-7020 · xc7z020clg400-2 \
    野火 PetaLinux 2022.2 · WM8960 \
    Vivado / Vitis HLS 2026.1 \
    Round30 持久启动版本 \
    #v(3mm)
    源基线：PL-20261027-01 \
    #text(size: 8pt, font: "Consolas")[a8f6f8f32b159eaea277354118220c633f31fbc2]
  ],
  city: [2026 年 11 月 3 日],
  year: none,
  add-pagebreaks: false,
  performers: none,
  manager: (position: none, name: none, title: none),
)

#set document(title: "基于 Zynq-7020 的实时 WORLD 语音处理 PS/PL 协同系统", author: "Pi-debug-cmd contributors")
#set text(font: ("Times New Roman", "SimSun"), lang: "zh", hyphenate: false)
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
