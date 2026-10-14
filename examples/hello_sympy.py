"""驗收 1：SymPy 能跑，而且能重現一個迷思概念。"""
from sympy import symbols, expand, simplify, solve, Eq

x = symbols("x")

# 正確：-(x - 2) = -x + 2
correct = expand(-(x - 2))

# 迷思 MC-ALG-003「負號只乘第一項」：-(x - 2) → -x - 2
def negate_first_term_only(a, b):
    return -a + b

buggy = negate_first_term_only(x, -2)

print("正確展開：", correct)
print("迷思寫法：", buggy)
print("兩者等價嗎？", simplify(correct - buggy) == 0)

# 代數字檢查（之後「認知衝突」就是這樣做）
print("代 x = 5：正確 =", correct.subs(x, 5), "，迷思 =", buggy.subs(x, 5))

# 解方程式 3 - (x - 2) = 4
print("正確解：", solve(Eq(3 + correct, 4), x))
print("迷思解：", solve(Eq(3 + buggy, 4), x))
