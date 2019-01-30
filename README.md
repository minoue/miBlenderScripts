# mayaっぽいkeymap

## Keymap変更点

### 3D View

**Alt navigation**

MayaのAltナビゲーション。

* 3D View → 3D view(globa) → Pan View → 'Alt Middle Mouse'に変更
* 3D View → 3D view(globa) → Zoom View → 'Alt Right Mouse'に変更


**F key focus**

フォーカスは頻繁に使うのでMayaと同じFキーに変更。デフォルトの'Numpad . 'は使用頻度の割に遠すぎる。

* 3D View → 3D View (global) → View Selected → Fに変更
* 3D View → Mesh → Mesh (global) → New keymap (view3d.view_selected)を作成
* 3D View → Mesh → Mesh (global) → Make Edge/Face → Disable


**Disable tweak move/translate**

マニピュレーターの外をドラッグするとオブジェクトが動いてしまうのを防止

* 3D View → 3D View(global) → Move(Tweak Left Any) → Disable
* 3D View → Object Mode → 3D View Tool: Transform → Disable

**WER object mode**

Mayaと同じWERキーによるマニピュレータの切り替え

* 3D View → Object Mode → Object Mode (Global) → New Keymap (W:Move)
* 3D View → Object Mode → Object Mode (Global) → New Keymap (E:Rotate)
* 3D View → Object Mode → Object Mode (Global) → New Keymap (R:Scale)

**WER mesh mode**

* 3D View → Mesh → Mesh (Global) → New Keymap (W:Move)
* 3D View → Mesh → Mesh (Global) → New Keymap (E:Rotate)
* 3D View → Mesh → Mesh (Global) → New Keymap (R:Scale)
* 3D View → Mesh → Mesh (Global) → Extrude and Move on Normals → Disable

**Box Selection while using transform manipulator**

マニピュレータを表示させた状態で追加のBox選択を可能にする

https://blender.stackexchange.com/questions/124195/blender-2-8-enter-select-box-mode-while-in-transform-mode

* 3D View → Object Mode → 3D View Tool: Move → Add New →
    * view3d.select_box
    * Tweak Left Any
    * Mode: New

これのみの場合Shiftドラッグによる追加と削除ができないのでShift用にもう一つキーマップを作製

* 3D View → Object Mode → 3D View Tool: Move → Add New →
    * view3d.select_box
    * Tweak Left Any (Shift modifier)
    * Mode: Difference
* 3D View Tool: Rotate, 3D View Tool: Scaleにも同じ変更

失われた本来の挙動をCtrlで呼び出せるようにする

* 3D View → Object Mode → 3D View Tool: Move → Move → Add Ctrl modifier
* 3D View → Object Mode → 3D View Tool: Rotate → Rotate → Add Ctrl modifier
* 3D View → Object Mode → 3D View Tool: Scale → Scale→ Add Ctrl modifier

**Box select**
通常のBox選択も同じ挙動に
* 3D View -> Object Mode -> 3D View Tool: Select Box -> 上から二つ目のModeをDifferenceに。

### View 2D

Altナビゲーション

* View 2D →  Zoom 2D View → "Alt Right Mouse"に変更
* View 2D → Add New → view2d.pan : Alt Middle Mouse
