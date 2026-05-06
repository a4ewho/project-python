from material import Material

aluminium = Material(
    name="Алюминий",
    rho=2700,
    c=900,
    k=207
)

glass = Material(
    name="Стекло",
    rho=2500,
    c=840,
    k=0.8
)

print(f"{aluminium.name}: α = {aluminium.alpha:.3e} м²/с")
print(f"{glass.name}: α = {glass.alpha:.3e} м²/с")