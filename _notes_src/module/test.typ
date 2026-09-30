#import "@preview/mmdr:0.1.0": mermaid

#mermaid("
  graph TD
    %% 定义五个点，内部空格确保圆圈等大
    A((&nbsp;1&nbsp;))
    B((&nbsp;2&nbsp;))
    C((&nbsp;3&nbsp;))
    D((&nbsp;4&nbsp;))
    E((&nbsp;5&nbsp;))

    %% 这里的连线顺序决定了它乱不乱
    %% 我们按五角星的轨迹连线：1-3, 3-5, 5-2, 2-4, 4-1
    A --- C
    C --- E
    E --- B
    B --- D
    D --- A

    %% 强制让某些点处于同一层级，防止排成竖长条
    subgraph 层级对齐 [ ]
      direction LR
      B --- C
      D --- E
    end
    style 层级对齐 fill:none,stroke:none
")