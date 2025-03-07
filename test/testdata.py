testdata_load_stations = {
    # Sample line from GHCN website
    "mock_response_text": "GME00129634  48.0458    8.4617  720.0    VILLINGEN-SCHWENNINGEN",
    # Simulates the content of the JSON file
    "read_data": '[{"ID": "GME00129634", "Latitude": 48.0458, "Longitude": 8.4617, "Elevation":720.0, "State":null, "Name":"VILLINGEN-SCHWENNINGEN"}]'
}

testdata_load_inventory = {
    # Sample line from GHCN website
    "mock_response_text": "GME00129634  48.0458    8.4617 TMAX 1947 2025\nGME00129634  48.0458    8.4617 TMIN 1947 2025\nGME00129634  48.0458    8.4617 PRCP 1947 2025\nGME00129634  48.0458    8.4617 SNWD 1947 2025",
    # Simulates the content of the JSON file
    "read_data": '{"GME00129634": {"TMAX": [1947, 2024], "TMIN": [1947, 2024]}}'
}

testdata_haversine = [
    # (lat1, lon1, lat2, lon2, expected)
    (48.0597, 8.4599, 48.0626, 8.5342, 5.5), # Villingen -> Schwenningen, 5.5 km expected
    (52.5200, 13.4050, 48.1351, 11.5820, 504.4), # Berlin -> Muenchen, 504.4 km expected
    (90, 0, -90, 0, 20015.1), # North Pole -> South Pole, 20015.1 km expected
    (48.0458, 8.4617, 48.0458, 8.4617, 0) # Same coordinates, 0 km expected
]

testdata_stations = [
    # Sample station data to test the find_nearest_stations function
    {"ID": "GME00129634", "Latitude": 48.0458, "Longitude": 8.4617}, # Villingen-Schwenningen
    {"ID": "GME00122458", "Latitude": 48.0242, "Longitude": 7.8353}, # Freiburg
    {"ID": "GME00129490", "Latitude": 48.5206, "Longitude": 9.0525}, # Tuebingen
    {"ID": "GME00129442", "Latitude": 48.3142, "Longitude": 9.2481}, # Trochtelfingen
    {"ID": "GME00127850", "Latitude": 52.5331, "Longitude": 13.3831} # Berlin-Mitte
]

testdata_inventory = {
    # Sample inventory data to test the find_nearest_stations function
    "GME00129634": {"TMAX": [1947, 2024], "TMIN": [1947, 2024]},
    "GME00122458": {"TMAX": [1881, 2024], "TMIN": [1881, 2024]},
    "GME00129490": {"TMAX": [1950, 1982], "TMIN": [1950, 1982]},
    "GME00129442": {"TMAX": [1947, 1973], "TMIN": [1947, 1973]},
    "GME00127850": {"TMAX": [1956, 1964], "TMIN": [1956, 1964]}
}

testdata_nearest_station = [
    # (user_lat, user_lon, radius, max_stations, start_year, end_year)
    {
        "input": [48.0458, 8.4617, 100, 5, 1956, 1964], # Villingen-Schwenningen, 100 km radius, max 5 stations
        "expected_ids": ["GME00129634", "GME00122458", "GME00129490", "GME00129442"] # 4 stations expected
    },
    {
        "input": [48.0458, 8.4617, 100, 3, 1956, 1964], # Villingen-Schwenningen, 100 km radius, max 3 stations
        "expected_ids": ["GME00129634", "GME00122458", "GME00129442"] # 3 stations expected
    },
    {
        "input": [47.3759, -31.2243, 1, 5, 1956, 1964], # Remote location in the sea, 1 km radius
        "expected_ids": [] # 0 stations expected
    }
]

testdata_download_weather = {
    # Sample data from GHCN website
    "mock_response_text": """GME00129634202001TMAX   57  E   -4  E   86  E   37  E   40  E   34  E   59  E   43  E   97  E   86  E   51  E   -2  E   51  E   68  E  113  E  123  E   83  E   43  E   16  E   17  E   40  E   67  E   46  E   63  E   87  E   93  E   40  E   47  E   39  E   81  E  112  E
GME00129634202001TMIN  -75  E  -61  E  -27  E   -4  E  -39  E  -52  E  -27  E  -25  E   12  E   30  E  -39  E  -64  E  -24  E  -30  E  -20  E  -21  E  -28  E  -18  E  -47  E  -42  E  -74  E  -74  E  -91  E  -55  E  -28  E  -37  E    4  E   -2  E  -20  E  -23  E   53  E
GME00129634202001PRCP    0  E    0  E   16  E    0  E    0  E    0  E    0  E    0  E    0  E    5  E    0  E    0  E    0  E    0  E    0  E    0  E   33  E    9  E    4  E    0  E    0  E    0  E    0  E    0  E    0  E    3  E   50  E  122  E   11  E   25  E    0  E
GME00129634202001SNWD    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   10  E   20  E   20  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   90  E   60  E    0  E
GME00129634202002TMAX  126  E  115  E  124  E   99  E   38  E   56  E   61  E   80  E  111  E  119  E   62  E   29  E   52  E   72  E   79  E  141  E  139  E   62  E   48  E   98  E   75  E  139  E  143  E  145  E  110  E   35  E   43  E   45  E   92  E-9999   -9999   
GME00129634202002TMIN   52  E   64  E   66  E   -7  E  -64  E  -85  E  -83  E  -64  E  -24  E   32  E    3  E  -10  E  -31  E  -16  E  -32  E   20  E   23  E   13  E  -14  E   -7  E  -22  E  -34  E   50  E   76  E   28  E  -42  E  -40  E  -30  E   15  E-9999   -9999   
GME00129634202002PRCP   95  E  280  E  329  E  105  E    0  E    0  E    0  E    0  E   25  E  328  E  100  E   31  E  127  E    3  E    0  E    0  E   46  E    2  E   41  E   23  E    0  E    5  E    4  E    0  E   80  E   85  E  196  E    1  E   71  E-9999   -9999   
GME00129634202002SNWD    0  E    0  E    0  E    0  E  120  E   80  E   70  E   60  E   50  E    0  E   10  E   50  E   60  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   20  E  120  E  200  E  130  E-9999   -9999   
GME00129634202003TMAX  108  E   66  E   48  E   67  E   52  E   46  E   51  E   90  E   82  E   88  E  131  E  146  E  100  E   95  E  127  E  167  E  149  E  184  E  184  E  162  E   79  E   68  E   63  E   63  E   60  E   70  E  131  E  156  E   39  E   27  E   65  E
GME00129634202003TMIN   20  E  -21  E  -10  E  -30  E   -5  E   14  E  -28  E  -32  E   -6  E  -13  E   63  E   36  E  -13  E  -27  E  -42  E  -22  E   24  E   -2  E    8  E   14  E    3  E  -30  E  -55  E  -58  E  -45  E  -47  E  -21  E  -14  E   -7  E  -53  E  -79  E
GME00129634202003PRCP    8  E   19  E    0  E    5  E  208  E   24  E    0  E    6  E    2  E   27  E    5  E    5  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    3  E   35  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   45  E    0  E    0  E
GME00129634202003SNWD   40  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   80  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   80  E    0  E
GME00129634202004TMAX  112  E  142  E  118  E  143  E  187  E  201  E  201  E  217  E  208  E  218  E  215  E  211  E  202  E   91  E  182  E  223  E  233  E  230  E  218  E  168  E  176  E  211  E  214  E  210  E  211  E  203  E  215  E  165  E  154  E  119  E-9999   
GME00129634202004TMIN  -66  E  -61  E  -37  E  -26  E  -22  E  -16  E    5  E    4  E   18  E   18  E   28  E   53  E   18  E  -20  E  -39  E  -15  E   36  E   60  E   42  E   69  E   60  E   30  E   11  E   16  E   48  E   11  E   71  E   85  E   47  E   55  E-9999   
GME00129634202004PRCP    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    6  E   12  E   87  E    0  E   12  E-9999   
GME00129634202004SNWD    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E-9999   
GME00129634202005TMAX  123  E  102  E  162  E  197  E  103  E  158  E  224  E  250  E  264  E  224  E  130  E  130  E   93  E   87  E  134  E  191  E  207  E  227  E  236  E  234  E  248  E  258  E  181  E  174  E  180  E  196  E  214  E  210  E  184  E  184  E  197  E
GME00129634202005TMIN   48  E    1  E  -20  E   46  E   75  E   18  E   -9  E   35  E   87  E  119  E   13  E    7  E   38  E   48  E   31  E    3  E   24  E   49  E   70  E   82  E   67  E   67  E   34  E   42  E   34  E   38  E   36  E   47  E   34  E   44  E   38  E
GME00129634202005PRCP   31  E   60  E    0  E    0  E   14  E    0  E    0  E    0  E   10  E   48  E  205  E    0  E  177  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   40  E   84  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E
GME00129634202006TMAX  236  E  257  E  238  E  183  E  132  E  152  E  150  E  180  E  111  E  151  E  190  E  255  E  236  E  160  E  206  E  184  E  163  E  207  E  165  E  198  E  231  E  245  E  259  E  274  E  273  E  254  E  264  E  243  E  218  E  244  E-9999   
GME00129634202006TMIN   55  E   63  E   80  E   93  E   88  E  101  E   82  E   75  E   92  E  101  E   93  E   81  E  108  E  116  E  102  E  102  E   73  E   48  E   84  E   79  E  100  E  104  E   88  E   96  E   91  E  117  E  112  E  138  E   97  E   84  E-9999   
GME00129634202006PRCP    0  E    0  E   91  E   30  E   68  E   76  E    1  E   17  E   22  E    7  E    0  E    0  E   10  E    1  E    0  E  225  E   38  E    1  E   25  E    0  E    0  E    0  E    0  E    0  E    0  E  124  E   22  E   14  E    3  E    0  E-9999   
GME00129634202007TMAX  293  E  219  E  209  E  249  E  266  E  205  E  229  E  251  E  289  E  270  E  215  E  236  E  250  E  259  E  177  E  151  E  181  E  238  E  269  E  292  E  267  E  272  E  271  E  232  E  272  E  246  E  310  E  278  E  282  E  322  E  348  E
GME00129634202007TMIN   91  E  139  E   96  E   77  E  123  E   74  E   44  E   62  E  100  E  119  E   92  E   66  E   72  E   85  E  121  E  120  E  117  E   80  E   79  E   89  E  120  E  118  E  107  E  106  E  101  E  122  E   88  E  140  E   94  E  106  E  120  E
GME00129634202007PRCP   37  E    0  E    0  E    0  E   15  E    0  E    0  E    0  E    0  E    4  E    0  E    0  E    0  E   13  E   34  E   35  E   23  E    0  E    0  E    0  E    0  E    0  E    0  E   12  E   15  E    4  E    0  E    2  E    0  E    0  E    0  E
GME00129634202008TMAX  321  E  219  E  202  E  185  E  230  E  270  E  303  E  306  E  311  E  317  E  307  E  305  E  240  E  211  E  269  E  283  E  225  E  246  E  242  E  293  E  329  E  234  E  217  E  216  E  219  E  233  E  229  E  215  E  145  E  121  E  164  E
GME00129634202008TMIN  142  E  148  E  116  E   84  E   58  E   80  E  121  E  123  E  125  E  129  E  148  E  140  E  134  E  137  E  125  E  122  E  132  E  111  E  100  E  150  E  134  E  135  E  104  E   81  E   62  E  109  E   68  E  106  E  106  E   92  E   83  E
GME00129634202008PRCP  168  E  155  E  199  E    3  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    2  E   74  E   92  E    0  E  143  E    6  E    0  E    0  E    9  E   43  E   31  E    0  E    0  E    0  E    0  E    0  E   69  E    3  E  243  E   48  E
GME00129634202009TMAX  175  E  192  E  219  E  257  E  258  E  172  E  193  E  231  E  259  E  235  E  253  E  256  E  275  E  291  E  307  E  269  E  222  E  209  E  249  E  258  E  241  E  233  E  204  E  200  E  104  E   59  E   97  E  145  E  125  E  186  E-9999   
GME00129634202009TMIN   98  E   89  E   52  E   75  E  108  E   86  E   83  E   46  E   56  E   71  E   98  E   89  E   83  E   81  E   90  E  109  E  117  E   85  E   55  E   86  E   74  E   91  E   95  E  100  E   50  E   30  E   20  E    1  E   68  E   30  E-9999   
GME00129634202009PRCP   24  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    4  E    2  E    7  E  116  E   87  E   55  E    0  E    0  E    0  E    0  E-9999   
GME00129634202010TMAX  154  E  167  E  107  E  163  E  109  E  134  E  119  E  155  E  171  E  101  E   83  E  103  E   99  E   91  E   64  E   83  E   82  E   86  E  113  E  142  E  175  E  179  E  125  E  141  E  151  E   92  E   90  E  112  E  104  E  120  E  150  E
GME00129634202010TMIN   43  E   80  E   38  E   57  E   47  E   70  E   54  E   46  E   70  E   14  E  -10  E   -4  E  -10  E    6  E   39  E   44  E   28  E   37  E    7  E    2  E   53  E   75  E  101  E   21  E   14  E   36  E   27  E   52  E   72  E   20  E   -4  E
GME00129634202010PRCP    4  E    0  E   82  E    7  E   55  E  166  E   39  E    0  E   18  E   16  E   13  E    0  E    0  E    3  E   55  E    7  E    3  E    0  E    0  E    0  E    0  E   79  E   54  E    0  E   53  E   68  E    8  E   55  E   37  E    0  E    0  E
GME00129634202010SNWD    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E
GME00129634202011TMAX  132  E  184  E  140  E   60  E   82  E   66  E  135  E  148  E  168  E  152  E  142  E  118  E  134  E  150  E  130  E   98  E  112  E  117  E  100  E   42  E   48  E   78  E   87  E   70  E   61  E   93  E  111  E   83  E    8  E    8  E-9999   
GME00129634202011TMIN   25  E  112  E   54  E   48  E   41  E  -10  E    6  E   19  E   16  E    1  E   27  E   21  E    7  E   19  E    5  E   41  E    3  E  -18  E    3  E  -29  E  -56  E  -53  E  -18  E   -7  E  -32  E  -40  E  -43  E  -54  E  -51  E  -42  E-9999   
GME00129634202011PRCP   30  E    0  E   43  E   10  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    1  E    0  E    0  E   28  E    0  E    0  E    0  E   86  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   35  E-9999   
GME00129634202011SNWD    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E-9999   
GME00129634202012TMAX   17  E    2  E    0  E   27  E    7  E   14  E   14  E   32  E    8  E   -7  E    3  E   22  E   36  E   35  E   55  E   86  E   49  E   86  E   88  E   88  E   66  E  121  E  106  E   72  E   15  E   -2  E    2  E   10  E   32  E   20  E   -1  E
GME00129634202012TMIN  -29  E  -19  E  -29  E  -25  E  -11  E   -2  E  -24  E  -30  E  -17  E  -26  E  -35  E   -3  E    1  E   -3  E    5  E  -10  E  -10  E    3  E  -27  E   19  E    4  E   62  E   62  E   -4  E  -28  E  -74  E  -78  E  -49  E  -31  E  -48  E  -53  E
GME00129634202012PRCP   12  E    1  E    0  E   29  E   44  E   85  E    0  E    8  E   37  E    0  E   18  E    3  E    0  E    0  E   21  E    0  E    0  E    0  E    0  E    1  E   23  E   35  E   69  E   45  E   16  E    0  E   67  E   86  E    5  E    2  E    9  E
GME00129634202012SNWD   40  E   40  E   40  E   40  E   70  E   80  E  110  E   90  E  100  E  140  E  130  E  130  E   70  E   40  E   30  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   20  E   20  E  160  E  200  E  170  E  150  E
GME00129634202101TMAX    8  E  -10  E   -6  E  -12  E  -16  E    1  E    6  E    2  E   -8  E  -15  E  -40  E    8  E   20  E   20  E  -24  E  -44  E   18  E    9  E   32  E   21  E   62  E   72  E    7  E    6  E   15  E    9  E   -8  E   79  E   76  E   46  E   41  E
GME00129634202101TMIN  -24  E  -24  E  -27  E  -34  E  -36  E  -36  E  -47  E  -95  E -115  E  -78  E -114  E -103  E  -35  E  -33  E -100  E  -95  E  -55  E  -64  E -111  E  -48  E  -18  E   -3  E  -22  E  -67  E  -46  E  -52  E  -55  E  -19  E   27  E   16  E   12  E
GME00129634202101PRCP    0  E   18  E    0  E    0  E    8  E   27  E    0  E    0  E    0  E    0  E    0  E   71  E  143  E  293  E   12  E    7  E    0  E    1  E    1  E    0  E   35  E   49  E   50  E   38  E   47  E    1  E   14  E  234  E  100  E   47  E   31  E
GME00129634202101SNWD  170  E  150  E  150  E  150  E  140  E  140  E  180  E  170  E  160  E  150  E  150  E  150  E  260  E  300  E  600  E  550  E  520  E  490  E  470  E  450  E  420  E  340  E  330  E  380  E  400  E  440  E  400  E  400  E  250  E  200  E  170  E
GME00129634202102TMAX   57  E   85  E   92  E   81  E  107  E   57  E   72  E   12  E   -1  E  -26  E  -61  E  -43  E  -40  E   10  E    8  E   83  E   96  E   95  E  113  E  137  E  180  E  175  E  175  E  180  E  189  E  165  E   76  E  100  E-9999   -9999   -9999   
GME00129634202102TMIN   20  E   10  E   48  E   15  E   23  E   11  E    2  E  -22  E  -31  E -100  E -148  E -158  E -147  E -175  E -113  E    2  E  -30  E  -38  E    0  E  -20  E  -37  E  -32  E  -11  E   -7  E  -20  E  -17  E  -12  E  -29  E-9999   -9999   -9999   
GME00129634202102PRCP   55  E  175  E  123  E    1  E    6  E    0  E   35  E   14  E   35  E   21  E    0  E    0  E    0  E    0  E    0  E   28  E    0  E   17  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E-9999   -9999   -9999   
GME00129634202102SNWD  150  E  100  E    0  E    0  E    0  E    0  E    0  E   10  E   40  E   80  E  120  E  100  E   90  E   80  E   80  E   80  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E-9999   -9999   -9999   
GME00129634202103TMAX  116  E  161  E  110  E  132  E   48  E   64  E   98  E   79  E   75  E   94  E  118  E   80  E   79  E   35  E   49  E   37  E   51  E   24  E   37  E   19  E   50  E   29  E   79  E  145  E  151  E  156  E   77  E  138  E  199  E  226  E  234  E
GME00129634202103TMIN  -55  E  -52  E  -16  E   23  E  -13  E  -48  E  -54  E  -45  E  -62  E  -19  E   28  E   14  E    6  E   -3  E    1  E    1  E  -19  E  -23  E  -48  E  -47  E  -29  E   -3  E  -30  E  -49  E  -32  E  -15  E    5  E  -32  E  -21  E   -7  E    4  E
GME00129634202103PRCP    0  E    0  E    0  E   44  E    1  E    0  E    0  E    0  E    0  E    0  E  231  E    4  E  156  E   38  E   37  E   20  E   23  E    0  E   11  E    1  E    0  E    0  E    0  E    0  E    0  E   50  E    0  E    0  E    0  E    0  E    0  E
GME00129634202103SNWD    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   40  E   40  E   20  E   40  E   20  E    0  E   10  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E
GME00129634202104TMAX  233  E  146  E   73  E  122  E  111  E   29  E   12  E   87  E  159  E  153  E  177  E   57  E   58  E   66  E   65  E   62  E   74  E   59  E   92  E  148  E  162  E  147  E  168  E  202  E  167  E  165  E  174  E  194  E  140  E   79  E-9999   
GME00129634202104TMIN   21  E   22  E  -19  E  -41  E  -35  E  -74  E  -45  E  -37  E  -43  E   11  E   38  E  -29  E  -50  E  -49  E  -20  E  -36  E  -30  E   12  E  -22  E   -5  E  -13  E    0  E  -23  E  -21  E   13  E   15  E  -11  E   -4  E   68  E   35  E-9999   
GME00129634202104PRCP    0  E    0  E    0  E    0  E   21  E   45  E    0  E    0  E    0  E    0  E  106  E    3  E    2  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   30  E    9  E  129  E-9999   
GME00129634202104SNWD    0  E    0  E    0  E    0  E    0  E   20  E   80  E    0  E    0  E    0  E    0  E   40  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E-9999   
GME00129634202105TMAX   65  E  103  E  127  E  148  E   98  E   78  E  108  E  172  E  257  E  208  E  166  E  118  E  142  E  159  E  127  E  135  E  121  E  130  E  155  E  148  E  123  E  151  E  157  E  145  E  140  E  106  E  149  E  188  E  193  E  186  E  212  E
GME00129634202105TMIN   31  E    3  E  -20  E    3  E   13  E   22  E   -3  E  -18  E   33  E   89  E   84  E   52  E   30  E    8  E   33  E   54  E   52  E   44  E   33  E   38  E   46  E   52  E   36  E   23  E   34  E   52  E   47  E   17  E   56  E   32  E   22  E
GME00129634202105PRCP  154  E   11  E    0  E   89  E   22  E  294  E   13  E    0  E    0  E    0  E   68  E    0  E    1  E    1  E   74  E  136  E   55  E   64  E    9  E    0  E  149  E   14  E    0  E   22  E   29  E   69  E    3  E    0  E    0  E    0  E    0  E
GME00129634202106TMAX  234  E  238  E  220  E  234  E  168  E  157  E  181  E  207  E  242  E  233  E  263  E  260  E  242  E  273  E  292  E  287  E  298  E  303  E  288  E  262  E  259  E  218  E  232  E  221  E  192  E  235  E  262  E  277  E  214  E  167  E-9999   
GME00129634202106TMIN   33  E   45  E  117  E  104  E  126  E  124  E  132  E  116  E  107  E   85  E   91  E  101  E   99  E   72  E   96  E  118  E  122  E  148  E  152  E  135  E  136  E  134  E  129  E  124  E  123  E  111  E  111  E  129  E  115  E   93  E-9999   
GME00129634202106PRCP    0  E    0  E   46  E   83  E   56  E   46  E  133  E    0  E   53  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E  170  E    5  E  333  E  116  E   33  E  124  E   28  E    4  E    0  E  102  E  149  E  119  E   19  E-9999   
GME00129634202107TMAX  175  E  225  E  240  E  214  E  213  E  230  E  205  E  179  E  224  E  239  E  218  E  254  E  155  E  188  E  194  E  210  E  222  E  245  E  268  E  252  E  263  E  266  E  270  E  239  E  201  E  227  E  231  E  220  E  239  E  270  E  226  E
GME00129634202107TMIN   95  E   72  E   81  E  128  E  118  E  105  E  132  E  129  E  111  E   87  E  105  E   85  E  105  E  100  E  116  E  121  E  150  E  131  E  134  E  111  E  105  E  114  E  111  E  138  E  122  E  117  E   94  E  112  E   93  E   97  E  116  E
GME00129634202107PRCP    0  E    0  E   28  E    6  E   10  E  187  E   30  E  105  E    0  E   30  E    0  E  309  E  126  E   86  E   16  E    4  E    7  E    0  E    0  E    0  E    0  E    0  E    0  E   89  E   83  E   69  E   32  E   31  E    0  E   10  E  143  E
GME00129634202108TMAX  159  E  207  E  165  E  164  E  183  E  206  E  162  E  197  E  213  E  256  E  272  E  295  E  290  E  301  E  277  E  205  E  187  E  207  E  211  E  249  E  268  E  191  E  201  E  172  E  214  E  168  E  187  E  161  E  160  E  174  E  181  E
GME00129634202108TMIN   98  E  101  E   78  E  106  E  107  E  107  E  104  E   79  E   63  E   82  E  103  E  114  E  146  E  148  E  144  E  112  E   81  E  114  E  109  E  118  E   95  E  101  E   83  E  102  E   86  E   61  E   86  E   87  E   89  E  110  E   88  E
GME00129634202108PRCP  166  E    0  E   25  E   18  E  128  E    0  E  104  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E  190  E   28  E    0  E    0  E    0  E    0  E    1  E   15  E    3  E    0  E    0  E    0  E    4  E    7  E   12  E   14  E    2  E
GME00129634202109TMAX  206  E  225  E  257  E  246  E  246  E  247  E  241  E  258  E  237  E  230  E  212  E  229  E  241  E  252  E  182  E  178  E  177  E  206  E  170  E  155  E  163  E  177  E  214  E  215  E  233  E  187  E  198  E  170  E  177  E  154  E-9999   
GME00129634202109TMIN   75  E   52  E   57  E   75  E   81  E   84  E   78  E   69  E  105  E  128  E   98  E   75  E   86  E   93  E  136  E  110  E   79  E   51  E   62  E   96  E   58  E   36  E   22  E   33  E   45  E  100  E   65  E   78  E   44  E   12  E-9999   
GME00129634202109PRCP    0  E    0  E    0  E    0  E   17  E    0  E    0  E    0  E    2  E   15  E  124  E    0  E    0  E   23  E   38  E   68  E    0  E    0  E   80  E    0  E    0  E    0  E    0  E    0  E    1  E   75  E   11  E    0  E   11  E    0  E-9999   
GME00129634202110TMAX  208  E  194  E  196  E  122  E  145  E  125  E  110  E  141  E  156  E  139  E  143  E   91  E  105  E  132  E  150  E  142  E  127  E  173  E  153  E  190  E  133  E  100  E  114  E  131  E  149  E  136  E  148  E  144  E  168  E   98  E  180  E
GME00129634202110TMIN    4  E   71  E   97  E   89  E   60  E   45  E   63  E   53  E   17  E   -3  E  -27  E   45  E    3  E  -20  E  -13  E   -6  E   -6  E   -9  E   23  E   44  E   75  E   -8  E  -13  E  -37  E  -16  E   16  E  -10  E   -4  E  -17  E  -15  E   56  E
GME00129634202110PRCP    0  E    0  E   28  E   97  E   11  E   21  E    0  E    0  E    0  E    0  E    0  E   32  E    0  E    0  E    0  E    0  E    0  E    0  E    1  E   86  E   37  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   15  E   57  E
GME00129634202110SNWD    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E
GME00129634202111TMAX  112  E   84  E   70  E   56  E   72  E   84  E   64  E   90  E   84  E  125  E  139  E  145  E   89  E   72  E   61  E   42  E   35  E   69  E  120  E   33  E   46  E   30  E   24  E    1  E   25  E   17  E   20  E   12  E    6  E   23  E-9999   
GME00129634202111TMIN   21  E    0  E    4  E   12  E   -1  E  -30  E  -33  E  -22  E  -39  E  -22  E  -19  E  -21  E  -17  E   46  E   22  E   18  E   21  E  -14  E  -31  E  -14  E  -19  E    4  E  -35  E  -51  E  -33  E  -14  E  -74  E  -38  E  -27  E  -19  E-9999   
GME00129634202111PRCP   31  E   20  E   17  E    1  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   12  E    1  E    0  E    1  E    0  E    0  E    0  E    0  E   14  E   21  E    0  E    0  E    0  E   20  E   47  E    6  E   16  E   31  E-9999   
GME00129634202111SNWD    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   10  E    0  E    0  E    0  E    0  E   40  E   80  E   90  E  120  E-9999   
GME00129634202112TMAX   55  E   30  E    7  E   57  E   27  E   30  E   32  E   12  E   25  E   12  E   20  E    5  E   48  E   35  E   19  E   29  E   53  E    8  E   63  E   18  E    5  E  -38  E   63  E   59  E   62  E   55  E   56  E   95  E  108  E  141  E   99  E
GME00129634202112TMIN   14  E  -18  E  -36  E  -14  E  -26  E  -32  E  -29  E   -6  E  -41  E  -43  E  -61  E  -88  E  -22  E  -41  E    3  E   -8  E   -1  E  -29  E  -56  E  -56  E  -88  E  -67  E  -67  E    4  E   15  E   16  E   25  E   23  E   50  E   71  E   12  E
GME00129634202112PRCP   67  E   22  E   94  E  142  E    2  E   16  E   31  E   12  E    0  E   57  E    4  E    0  E    0  E    0  E    0  E    1  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E   41  E   11  E   27  E   46  E  140  E   33  E    0  E    0  E
GME00129634202112SNWD   80  E    0  E   40  E   60  E   20  E    0  E   50  E   60  E   50  E   50  E  120  E  120  E  100  E   60  E   50  E   40  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E    0  E"""
}

testdata_calculate_means = {
    # Sample data
    "weather_data": {
        "2024-01-01": {"TMAX": 10.0, "TMIN": 3.0},
        "2024-01-02": {"TMAX": 12.0, "TMIN": 4.0},
        "2024-01-03": {"TMAX": 8.0, "TMIN": 2.0},
        "2024-07-01": {"TMAX": 30.0, "TMIN": 15.0}
    },
    "first_year": 2023,
    "last_year": 2024,
    "latitude": 50,
    "expected_result": {
        "entire_year": {
            2024: {"TMAX": 15.0, "TMIN": 6.0}
        },
        "winter": {
            2024: {"TMAX": 10.0, "TMIN": 3.0}
        },
        "spring": {},
        "summer": {
            2024: {"TMAX": 30.0, "TMIN": 15.0}
        },
        "autumn": {}
    }
}

testdata_fill_input_fields = {
    # Sample input
    "latitude": "48.0458",
    "longitude": "8.4617",
    "radius": "50",
    "maxStations": "5",
    "startYear": "2010",
    "endYear": "2020"
}
