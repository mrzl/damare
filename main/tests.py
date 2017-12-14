import fabric_helper, lyrik


def test_uname():
    fab = fabric_helper.FabricHelper()
    uname_return = fab.uname()

    expected_lyrik_return = 'Linux lyrik 4.4.0-98-generic #121-Ubuntu SMP Tue ' \
                            'Oct 10 14:24:03 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux'

    print(expected_lyrik_return)
    print(uname_return)
    assert uname_return == expected_lyrik_return


def test_ls():
    l = lyrik.Lyrik()
    model_list = l.style_images()
    l.disconnect()
    print(model_list)
    print(type(model_list))

if __name__ == '__main__':
    test_ls()