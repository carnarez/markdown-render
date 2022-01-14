All examples taken from [this page](https://github.com/mermaid-js/mermaid/blob/develop/docs/theming.md).

[TOC]

# Class diagram

```mermaid
classDiagram
  Animal "1" <|-- Duck
  Animal <|-- Fish
  Animal <--o Zebra
  Animal : +int age
  Animal : +String gender
  Animal: +isMammal()
  Animal: +mate()
  class Duck{
    +String beakColor
    +swim()
    +quack()
  }
  class Fish{
    -int sizeInFeet
    -canEat()
  }
  class Zebra{
    +bool is_wild
    +run()
  }
```

# Entity Relations diagram

```mermaid
erDiagram
  CUSTOMER }|..|{ DELIVERY-ADDRESS : has
  CUSTOMER ||--o{ ORDER : places
  CUSTOMER ||--o{ INVOICE : "liable for"
  DELIVERY-ADDRESS ||--o{ ORDER : receives
  INVOICE ||--|{ ORDER : covers
  ORDER ||--|{ ORDER-ITEM : includes
  PRODUCT-CATEGORY ||--|{ PRODUCT : contains
  PRODUCT ||--o{ ORDER-ITEM : "ordered in"
```

# Flowchart

```mermaid
graph TD
  A[Christmas] -->|Get money| B(Go shopping)
  B --> C{Let me think}
  B --> G[/Another/]
  C ==>|One| D[Laptop]
  C -->|Two| E[iPhone]
  C -->|Three| F[fa:fa-car Car]
  subgraph section
    C
    D
    E
    F
    G
  end
```

```mermaid
flowchart LR;
%% the simplest of flowcharts
  A --> B
  B --> C
  C --> D
%% example with various node shapes
  simple
  less-simple
  normal[This is the text in the box]
  rounded(This is the text in the box)
  stadium([This is the text in the box])
  subroutine[[This is the text in the box]]
  cylinder[(Database)]
  circle1((This is the text in the circle))
  circle2(("This is the text --> ((circle))"))
  asymmetric>This is the text in the box]
  rhombus{This is the text in the box}
  hexagon{{This is the text in the box}}
  parallelogram[/This is the text in the box/]
  paralellogram-alt[\This is the text in the box\]
  trapezoid[/Christmas\]
  trapezoid-alt[\Go shopping/]
%% example with various link shapes
  A-->a
  B --- b
  C-- This is the text! ---c
  D{text}--o|This is the text|d
  E-->|text|e
  F-- text -->f
  G-.->g
  H-..-> h
  I ==> i
  J == text ==> j
  K --o k
  L --x l
  M o--o m
  N <--> n
  P x--x p
  Q x---|"Complicated [(text)] <--- test"| q
%% convoluted linking
  A -- text1 --> B -- text2 --> C
  D --> E & F --> G
  H & I & J --> K & L
  L x--- o
  O x--x o
%% with subgraph
  A1[Christmas] -->|Get money| B1(Go shopping)
  B1 --> C1{Let me think}
  B1 --> G1[/Another/]
  C1 ==>|One| D1[Laptop]
  C1 -->|Two| E1[iPhone]
  C1 -->|Three| F1[fa:fa-car Car]
  subgraph section
    subgraph subsection
      C1
      D1
    end
    subgraph subsection
      E1
      F1
      G1
    end
  end
  H1 --> I1[(Text?)]
  subgraph paragraph
    X --> Y
  end
```

# Gantt

```mermaid
gantt
  dateFormat                          YYYY-MM-DD
  title                               Adding GANTT diagram functionality to mermaid
  excludes                            :excludes the named dates/days from being included in a charted task

  section A section
  Completed task                      :done,    des1, 2014-01-06,2014-01-08
  Active task                         :active,  des2, 2014-01-09, 3d
  Future task                         :         des3, after des2, 5d
  Future task2                        :         des4, after des3, 5d

  section Critical tasks
  Completed task in the critical line :crit, done, 2014-01-06,24h
  Implement parser and jison          :crit, done, after des1, 2d
  Create tests for parser             :crit, active, 3d
  Future task in critical line        :crit, 5d
  Create tests for renderer           :2d
  Add to mermaid                      :1d

  section Documentation
  Describe gantt syntax               :active, a1, after des1, 3d
  Add gantt diagram to demo page      :after a1  , 20h
  Add another diagram to demo page    :doc1, after a1  , 48h

  section Last section
  Describe gantt syntax               :after doc1, 3d
  Add gantt diagram to demo page      :20h
  Add another diagram to demo page    :48h
```

# Requirement diagram

```mermaid
requirementDiagram
  requirement test_req {
    id: 1
    text: the test text.
    risk: high
    verifymethod: test
  }
  element test_entity {
    type: simulation
  }
  test_entity - satisfies -> test_req
```

# Sequence diagram

```mermaid
sequenceDiagram
  autonumber
  par Action 1
    Alice->>John: Hello John, how are you?
  and Action 2
    Alice->>Bob: Hello Bob, how are you?
  end
  Alice->>+John: Hello John, how are you?
  Alice->>+John: John, can you hear me?
  John-->>-Alice: Hi Alice, I can hear you!
  Note right of John: John is perceptive
  John-->>-Alice: I feel great!
      loop Every minute
        John-->Alice: Great!
    end
```

# State diagram

```mermaid
stateDiagram
  [*] --> Active

  state Active {
    [*] --> NumLockOff
    NumLockOff --> NumLockOn : EvNumLockPressed
    NumLockOn --> NumLockOff : EvNumLockPressed
    --
    [*] --> CapsLockOff
    CapsLockOff --> CapsLockOn : EvCapsLockPressed
    CapsLockOn --> CapsLockOff : EvCapsLockPressed
    --
    [*] --> ScrollLockOff
    ScrollLockOff --> ScrollLockOn : EvCapsLockPressed
    ScrollLockOn --> ScrollLockOff : EvCapsLockPressed
  }
  state SomethingElse {
    A --> B
    B --> A
  }

  Active --> SomethingElse
  note right of SomethingElse : This is the note to the right.

  SomethingElse --> [*]
```

```mermaid
stateDiagram-v2
  [*] --> Active

  state Active {
    [*] --> NumLockOff
    NumLockOff --> NumLockOn : EvNumLockPressed
    NumLockOn --> NumLockOff : EvNumLockPressed
    --
    [*] --> CapsLockOff
    CapsLockOff --> CapsLockOn : EvCapsLockPressed
    CapsLockOn --> CapsLockOff : EvCapsLockPressed
    --
    [*] --> ScrollLockOff
    ScrollLockOff --> ScrollLockOn : EvCapsLockPressed
    ScrollLockOn --> ScrollLockOff : EvCapsLockPressed
  }
  state SomethingElse {
    A --> B
    B --> A
  }

  Active --> SomethingElse2
  note right of SomethingElse2 : This is the note to the right.

  SomethingElse2 --> [*]
```

# User journey diagram

```mermaid
journey
  title My working day
  section Go to work
    Make tea: 5: Me
    Go upstairs: 3: Me
    Do work: 1: Me, Cat
  section Go home
    Go downstairs: 5: Me
    Sit down: 5: Me
```
