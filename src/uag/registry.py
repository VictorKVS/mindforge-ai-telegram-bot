from providers.fake_shop import FakeShop

PROVIDERS = {
    "magazin_test_ctroika": FakeShop()
}

def get_provider(name: str):
    return PROVIDERS.get(name)
