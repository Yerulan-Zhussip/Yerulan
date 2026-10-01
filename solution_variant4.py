import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 1. Динамикалық жүйені анықтау
def system(x, t):
    x1, x2 = x
    dx1dt = 4 * x1 + x2 - 2
    dx2dt = -2 * x1 + 5 * x2 + 4
    return [dx1dt, dx2dt]

# 2. Тепе-теңдік нүктесі (Аналитикалық шешім бойынша)
# 4*x1 + x2 - 2 = 0
# -2*x1 + 5*x2 + 4 = 0
# x1* = 7/11 ≈ 0.636363, x2* = -6/11 ≈ -0.545455
x1_eq = 7 / 11
x2_eq = -6 / 11

# 3. Фазалық кеңістік шекарасы
x1_min, x1_max = -3, 4
x2_min, x2_max = -4, 3

# Тор (Grid) құру
grid_points = 20
x1_vals = np.linspace(x1_min, x1_max, grid_points)
x2_vals = np.linspace(x2_min, x2_max, grid_points)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# Бағыттар өрісін (Vector Field) есептеу
dX1 = 4 * X1 + X2 - 2
dX2 = -2 * X1 + 5 * X2 + 4

# Өріс векторларын нормализациялау (бағыттарды анық көрсету үшін)
magnitude = np.sqrt(dX1**2 + dX2**2)
# Нөлге бөлуден сақтану
magnitude[magnitude == 0] = 1
dX1_norm = dX1 / magnitude
dX2_norm = dX2 / magnitude

# 4. Бастапқы шарт және сантық шешу (odeint)
x0 = [-0.7, 1.6]
t = np.linspace(0, 2, 200) # График үшін жиі нүктелер
sol = odeint(system, x0, t)

# Негізгі уақыт нүктелеріндегі сандық нәтижелерді шығару
t_table = np.linspace(0, 2, 11)
sol_table = odeint(system, x0, t_table)

print("=== 4-НҰСҚА: САНДЫҚ ШЕШУ НӘТИЖЕЛЕРІ (odeint) ===")
print(f"{'t':>6} | {'x1(t)':>12} | {'x2(t)':>12}")
print("-" * 36)
for ti, xi in zip(t_table, sol_table):
    print(f"{ti:6.2f} | {xi[0]:12.6f} | {xi[1]:12.6f}")

# 5. Фазалық портрет пен траекторияны бейнелеу
plt.figure(figsize=(10, 8))

# Векторлық өрісті (Quiver) салу
plt.quiver(X1, X2, dX1_norm, dX2_norm, color='gray', alpha=0.6, pivot='mid', label='Бағыттар өрісі')

# Фазалық траекторияны салу
plt.plot(sol[:, 0], sol[:, 1], 'b-', linewidth=2.5, label='Фазалық траектория (x(0)=[-0.7, 1.6])')

# Бастапқы нүктені белгілеу
plt.plot(x0[0], x0[1], 'go', markersize=8, label=f'Бастапқы шарт M0({x0[0]}, {x0[1]})')

# Тепе-теңдік нүктесін белгілеу
plt.plot(x1_eq, x2_eq, 'r*', markersize=14, label=f'Тепе-теңдік нүктесі M*({x1_eq:.3f}, {x2_eq:.3f})')

# График безендірулері
plt.title('4-нұсқа: Динамикалық жүйенің фазалық портреті және траекториясы', fontsize=14, pad=15)
plt.xlabel('$x_1$', fontsize=12)
plt.ylabel('$x_2$', fontsize=12)
plt.xlim([x1_min, x1_max])
plt.ylim([x2_min, x2_max])
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper left', fontsize=10)

# Суретті сақтау
plt.savefig('phase_portrait_variant4.png', dpi=300, bbox_inches='tight')
print("\nГрафик 'phase_portrait_variant4.png' файлына сәтті сақталды.")
