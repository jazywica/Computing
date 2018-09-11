# -*- encoding: utf-8 -*-
""" Template testing suite for Project_3 - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # imports testing engine
import _01_Project_3 as pro  # imports the algorithms we are going to test
import alg_cluster  # imports the Cluster class
import urllib2


def run_suite(cl):
    """ Some informal testing code """

    def load_data_table(data_url):
        """ Import a table of county-based cancer risk data from a csv format file """
        data_file = urllib2.urlopen(data_url)
        data = data_file.read()
        data_lines = data.split('\n')  # sample line: '01073, 704.191210749, 411.014665198, 662047, 7.3e-05'
        print "Loaded", len(data_lines), "data points"
        data_tokens = [line.split(',') for line in data_lines]  # <type 'list'>: [['01073', ' 704.191210749', ' 411.014665198', ' 662047', ' 7.3e-05\r'], <type 'list'>: ['06059', ' 113.997715586', ...], ... []]
        return [cl.Cluster(tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])) for tokens in data_tokens]  # formats the string to: Cluster('01073', ' 704.191210749', ' 411.014665198', ' 662047', ' 7.3e-05\r')

    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_24_URL = DIRECTORY + "data_clustering/unifiedCancerData_24.csv"
    DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
    DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"

    suite = poc_simpletest.TestSuite()  # create a TestSuite object
    print("\nSTARTING TESTS:")


    # 1. check the basic methods of the Cluster class
    obj = cl.Cluster(set(['01067']), 100, 100, 1, 1)
    suite.run_test(obj.distance(cl.Cluster(set(['01068']), 100, 105, 1, 1)), 5, "Test #1a: 'distance' method")

    obj = cl.Cluster(set(['01067']), -100, -100, 1, 0.5)
    suite.run_test_no_return(obj.merge_clusters(cl.Cluster(set(['01068']), 100, 100, 9, 0.5)), obj.vert_center(), obj.vert_center() == 80, "Test #1b: 'merge_cls' method")  # (0.1 * -100) + (0.9 * 100) = 80
    obj = cl.Cluster(set(['01067']), -100, -100, 1, 0.5)
    suite.run_test_no_return(obj.merge_clusters(cl.Cluster(set(['01068']), 100, 100, 9, 0.5)), obj.averaged_risk(), obj.averaged_risk() == 0.5, "Test #1c: 'merge_cls' method")  # (0.1 * 0.5) + (0.9 * 0.5) = 0.5
    obj = cl.Cluster(set(['01067']), -100, -100, 10, 0.5)
    suite.run_test_no_return(obj.merge_clusters(cl.Cluster(set(['01068']), 0, 0, 0, 0)), obj.vert_center(), obj.vert_center() == -100, "Test #1d: 'merge_cls' method")  # if one cluster is 0, then the other is not changed
    suite.run_test_no_return(obj.merge_clusters(cl.Cluster(set(['01068']), 0, 0, 0, 0)), obj.total_population(), obj.total_population() == 10, "Test #1e: 'merge_cls' method")
    suite.run_test_no_return(obj.merge_clusters(cl.Cluster(set(['01068']), 0, 0, 0, 0)), obj.averaged_risk(), obj.averaged_risk() == 0.5, "Test #1f: 'merge_cls' method")


    # 2. check the basic methods of the program directly
    p1 = cl.Cluster(set(['1']), -70, 0, 1, 0.5); p2 = cl.Cluster(set(['2']), -50, 0, 1, 0.5); p3 = cl.Cluster(set(['3']), -40, 0, 1, 0.5); p4 = cl.Cluster(set(['4']), -1, 0, 1, 0.5)
    p5 = cl.Cluster(set(['5']), 1, 0, 1, 0.5); p6 = cl.Cluster(set(['6']), 40, 0, 1, 0.5); p7 = cl.Cluster(set(['7']), 50, 0, 1, 0.5); p8 = cl.Cluster(set(['8']), 70, 0, 1, 0.5)

    list_4 = [p1, p2, p3, p4]
    suite.run_test(pro.pair_distance(list_4, 0, 2), (30.0, 0, 2), "Test #2a: 'pair_distance' method")  # here we check the distance between index 0 and 2
    list_24 = load_data_table(DATA_24_URL)
    suite.run_test(pro.pair_distance(list_24, 0, 10), (288.81290749279157, 0, 10), "Test #2b: 'pair_distance' method")

    list_8 = [p1, p2, p3, p4, p5, p6, p7, p8]
    suite.run_test(pro.slow_closest_pair(list_8), (2.0, 3, 4), "Test #2c: 'slow_closest_pair' method")


    # 3. check the fast 'closest pair' method
    p11 = cl.Cluster(set(['11']), -100, 3, 1, 0.5); p12 = cl.Cluster(set(['12']), -50, 2, 1, 0.5); p13 = cl.Cluster(set(['13']), -40, 1, 1, 0.5); p14 = cl.Cluster(set(['14']), -1, 0, 1, 0.5)
    p15 = cl.Cluster(set(['15']), 1, 0, 1, 0.5); p16 = cl.Cluster(set(['16']), 40, -1, 1, 0.5); p17 = cl.Cluster(set(['17']), 50, -2, 1, 0.5); p18 = cl.Cluster(set(['18']), 100, -3, 1, 0.5)

    list_8a = [p11, p12, p13, p14, p15, p16, p17, p18]
    suite.run_test(pro.closest_pair_strip(list_8a, 0, 50), (2.0, 3, 4), "Test #3a: 'closest_pair_strip' method")
    suite.run_test(pro.closest_pair_strip([cl.Cluster(set([]), 1.0, 1.0, 1, 0), cl.Cluster(set([]), 1.0, 5.0, 1, 0), cl.Cluster(set([]), 1.0, 4.0, 1, 0), cl.Cluster(set([]), 1.0, 7.0, 1, 0)], 1.0, 3.0), (1.0, 1, 2), "Test #3b: 'closest_pair_strip' method")
    suite.run_test(pro.closest_pair_strip([cl.Cluster(set([]), 0.32, 0.16, 1, 0), cl.Cluster(set([]), 0.39, 0.4, 1, 0), cl.Cluster(set([]), 0.54, 0.8, 1, 0), cl.Cluster(set([]), 0.61, 0.8, 1, 0), cl.Cluster(set([]), 0.76, 0.94, 1, 0)], 0.465, 0.07), (float('inf'), -1, -1), "Test #3c: 'closest_pair_strip' method")

    suite.run_test(pro.fast_closest_pair(list_8), (2.0, 3, 4), "Test #3d: 'fast_closest_pair' method")
    suite.run_test(pro.fast_closest_pair([cl.Cluster(set([]), 0.02, 0.39, 1, 0), cl.Cluster(set([]), 0.19, 0.75, 1, 0), cl.Cluster(set([]), 0.35, 0.03, 1, 0), cl.Cluster(set([]), 0.73, 0.81, 1, 0), cl.Cluster(set([]), 0.76, 0.88, 1, 0), cl.Cluster(set([]), 0.78, 0.11, 1, 0)]), (0.07615773105863904, 3, 4), "Test #3e: 'fast_closest_pair' indexed version method")

    list_long = [cl.Cluster(set(['06081']), 52.6171444847, 262.707477827, 707161, 5.6e-05), cl.Cluster(set(['06075']), 52.7404001225, 254.517429395, 776733, 8.4e-05), cl.Cluster(set(['06001']), 61.782098866, 259.312457296, 1443741, 7e-05), cl.Cluster(set(['06085']), 63.1509653633, 270.516712105, 1682585, 6.3e-05), cl.Cluster(set(['06021']), 65.2043358182, 213.245337355, 26453, 6.9e-05), cl.Cluster(set(['06113']), 68.2602083189, 236.862609218, 168660, 5.9e-05), cl.Cluster(set(['06101']), 74.2003718491, 229.646592975, 78930, 5.6e-05), cl.Cluster(set(['06067']), 74.3547338322, 245.49501455, 1223499, 6.1e-05), cl.Cluster(set(['06083']), 76.0382837186, 340.420376302, 399347, 6.4e-05), cl.Cluster(set(['06089']), 77.359494209, 188.945068958, 163256, 5.7e-05), cl.Cluster(set(['41067']), 92.2254623376, 76.2593957841, 445342, 7.3e-05), cl.Cluster(set(['06111']), 93.4973310868, 344.590570899, 753197, 5.8e-05), cl.Cluster(set(['06019']), 95.6093812211, 290.162708843, 799407, 6.4e-05), cl.Cluster(set(['06039']), 97.2145136451, 278.975077449, 123109, 6e-05), cl.Cluster(set(['41051']), 103.293707198, 79.5194104381, 660486, 9.3e-05), cl.Cluster(set(['41005']), 103.421444616, 88.318590492, 338391, 6.6e-05), cl.Cluster(set(['06029']), 103.787886113, 326.006585349, 661645, 9.7e-05), cl.Cluster(set(['53011']), 104.00046468, 74.0182527309, 345238, 6.4e-05), cl.Cluster(set(['06037']), 105.369854549, 359.050126004, 9519338, 0.00011), cl.Cluster(set(['06107']), 108.085024898, 306.351832438, 368021, 5.8e-05), cl.Cluster(set(['06059']), 113.997715586, 368.503452566, 2846289, 9.8e-05), cl.Cluster(set(['53033']), 125.27486023, 39.1497730391, 1737034, 5.8e-05), cl.Cluster(set(['06073']), 129.2075529, 387.064888184, 2813833, 6.6e-05), cl.Cluster(set(['06065']), 146.410389633, 374.21707964, 1545387, 6.1e-05), cl.Cluster(set(['06071']), 148.402461892, 350.061039619, 1709434, 7.7e-05), cl.Cluster(set(['06025']), 156.397958859, 393.161127277, 142361, 5.6e-05), cl.Cluster(set(['04013']), 214.128077618, 396.893960776, 3072149, 6.8e-05), cl.Cluster(set(['08031']), 371.038986573, 266.847932979, 554636, 7.9e-05), cl.Cluster(set(['08001']), 379.950978294, 265.078784954, 363857, 6.6e-05), cl.Cluster(set(['08005']), 380.281283151, 270.268826873, 487967, 5.9e-05), cl.Cluster(set(['31109']), 516.78216337, 250.188023316, 250291, 6.1e-05), cl.Cluster(set(['31055']), 525.799353573, 238.14275337, 463585, 6.2e-05), cl.Cluster(set(['48201']), 540.54731652, 504.62993865, 3400578, 6e-05), cl.Cluster(set(['48245']), 565.746895809, 504.541799993, 252051, 5.7e-05), cl.Cluster(set(['27053']), 570.131597541, 151.403325043, 1116200, 5.8e-05), cl.Cluster(set(['22017']), 570.826412839, 442.202574191, 252161, 6.2e-05), cl.Cluster(set(['27123']), 576.516685202, 151.219277482, 511035, 5.6e-05), cl.Cluster(set(['19163']), 621.490118929, 227.666851619, 158668, 5.6e-05), cl.Cluster(set(['29189']), 629.170659449, 297.571839563, 1016315, 6e-05), cl.Cluster(set(['28027']), 631.700027283, 400.68741948, 30622, 6e-05), cl.Cluster(set(['29510']), 632.327321169, 297.184524592, 348189, 6.9e-05), cl.Cluster(set(['28049']), 638.051593606, 445.785870317, 250800, 6e-05), cl.Cluster(set(['22071']), 651.338581076, 496.465402252, 484674, 6.4e-05), cl.Cluster(set(['28159']), 663.514261498, 425.274137823, 20160, 5.9e-05), cl.Cluster(set(['55079']), 664.855000617, 192.484141264, 940164, 7.4e-05), cl.Cluster(set(['17031']), 668.978975824, 219.400257219, 5376741, 6.1e-05), cl.Cluster(set(['47037']), 700.009323976, 350.107265446, 569891, 6.1e-05), cl.Cluster(set(['01073']), 704.191210749, 411.014665198, 662047, 7.3e-05), cl.Cluster(set(['01117']), 709.193528999, 417.394467797, 143293, 5.6e-05), cl.Cluster(set(['21111']), 715.347723878, 301.167740487, 693604, 5.9e-05), cl.Cluster(set(['01101']), 720.281573781, 440.436162917, 223510, 5.7e-05), cl.Cluster(set(['01015']), 723.907941153, 403.837487318, 112249, 5.6e-05), cl.Cluster(set(['47065']), 732.643747577, 370.017730905, 307896, 6.1e-05), cl.Cluster(set(['13313']), 737.308367745, 378.040993858, 83525, 5.6e-05), cl.Cluster(set(['01113']), 740.385154867, 436.939588695, 49756, 5.6e-05), cl.Cluster(set(['26125']), 743.036942153, 192.129690868, 1194156, 5.7e-05), cl.Cluster(set(['13215']), 745.265661102, 430.987078939, 186291, 5.9e-05), cl.Cluster(set(['26163']), 746.37046732, 200.570021537, 2061162, 6.4e-05), cl.Cluster(set(['13067']), 747.238620236, 397.293799252, 607751, 6.4e-05), cl.Cluster(set(['13121']), 750.160287596, 399.907752014, 816006, 7e-05), cl.Cluster(set(['13063']), 752.853876848, 406.722877803, 236517, 6.6e-05), cl.Cluster(set(['47093']), 753.012743594, 348.235180569, 382032, 5.6e-05), cl.Cluster(set(['13089']), 754.465443436, 400.059456026, 665865, 6.8e-05), cl.Cluster(set(['13151']), 756.589546538, 407.288873768, 119341, 5.6e-05), cl.Cluster(set(['13135']), 758.038826857, 395.110327675, 588448, 6.3e-05), cl.Cluster(set(['13247']), 758.37864157, 402.49780372, 70111, 5.6e-05), cl.Cluster(set(['12073']), 762.463896365, 477.365342219, 239452, 6.1e-05), cl.Cluster(set(['21019']), 768.726553092, 290.270551648, 49752, 5.8e-05), cl.Cluster(set(['39035']), 776.351457758, 216.558042612, 1393978, 5.8e-05), cl.Cluster(set(['51520']), 784.05333332, 328.847863787, 17367, 5.6e-05), cl.Cluster(set(['13245']), 796.799727342, 404.391349655, 199775, 5.9e-05), cl.Cluster(set(['54009']), 799.221537984, 240.153315109, 25447, 7.7e-05), cl.Cluster(set(['42003']), 809.003419092, 233.899638663, 1281666, 6.1e-05), cl.Cluster(set(['37119']), 813.724315147, 356.853362811, 695454, 5.6e-05), cl.Cluster(set(['51775']), 820.111751617, 307.695502162, 24747, 5.8e-05), cl.Cluster(set(['51770']), 821.912162221, 307.548990323, 94911, 6.5e-05), cl.Cluster(set(['51680']), 835.264653899, 302.326633095, 65269, 5.8e-05), cl.Cluster(set(['51820']), 837.346467474, 285.851438947, 19520, 5.8e-05), cl.Cluster(set(['51840']), 845.843602685, 258.214178983, 23585, 7.1e-05), cl.Cluster(set(['51059']), 863.064397845, 262.414412378, 969749, 5.7e-05), cl.Cluster(set(['24031']), 863.180208628, 255.65657011, 873341, 6.5e-05), cl.Cluster(set(['51610']), 864.078108667, 261.655667801, 10377, 6.9e-05), cl.Cluster(set(['51760']), 865.424050159, 293.735963553, 197790, 8.6e-05), cl.Cluster(set(['51013']), 865.681962839, 261.222875114, 189453, 7.7e-05), cl.Cluster(set(['51087']), 866.389610525, 292.780704494, 262300, 6.3e-05), cl.Cluster(set(['51510']), 866.572477724, 262.734686855, 128283, 6.8e-05), cl.Cluster(set(['24027']), 867.127763298, 252.141340019, 247842, 6e-05), cl.Cluster(set(['11001']), 867.470401202, 260.460974222, 572059, 7.7e-05), cl.Cluster(set(['51570']), 868.048530719, 299.360459202, 16897, 5.6e-05), cl.Cluster(set(['24033']), 870.786325575, 261.829970016, 801515, 6.4e-05), cl.Cluster(set(['24005']), 871.921241442, 246.932531615, 754292, 6.1e-05), cl.Cluster(set(['24510']), 872.946822486, 249.834427518, 651154, 7.4e-05), cl.Cluster(set(['42101']), 894.72914873, 227.900547575, 1517550, 5.8e-05), cl.Cluster(set(['34007']), 899.061431482, 232.054232622, 508932, 5.7e-05), cl.Cluster(set(['34031']), 904.161746346, 201.712206531, 489049, 6.3e-05), cl.Cluster(set(['34023']), 904.976453741, 215.001458637, 750162, 5.9e-05), cl.Cluster(set(['34039']), 905.587082153, 210.045085725, 522541, 7.3e-05), cl.Cluster(set(['34013']), 906.236730753, 206.977429459, 793633, 7.1e-05), cl.Cluster(set(['34003']), 907.896066895, 202.302470427, 884118, 6.9e-05), cl.Cluster(set(['36085']), 908.749199508, 211.307161341, 443728, 7e-05), cl.Cluster(set(['34017']), 909.08042421, 207.462937763, 608975, 9.1e-05), cl.Cluster(set(['36061']), 911.072622034, 205.783086757, 1537195, 0.00015), cl.Cluster(set(['36047']), 911.595580089, 208.928374072, 2465326, 9.8e-05), cl.Cluster(set(['36119']), 912.141547823, 196.592589736, 923459, 6.5e-05), cl.Cluster(set(['36005']), 912.315497328, 203.674106811, 1332650, 0.00011), cl.Cluster(set(['36081']), 913.462051588, 207.615750359, 2229379, 8.9e-05), cl.Cluster(set(['36059']), 917.384980291, 205.43647538, 1334544, 7.6e-05), cl.Cluster(set(['09003']), 925.917212741, 177.152290276, 857183, 5.7e-05), cl.Cluster(set(['36103']), 929.241649488, 199.278463003, 1419369, 6.3e-05), cl.Cluster(set(['25017']), 943.405755498, 156.504310828, 1465396, 5.6e-05), cl.Cluster(set(['25025']), 950.299079197, 158.007070966, 689807, 7e-05)]
    suite.run_test(pro.fast_closest_pair(list_long), (1.266216002018164, 79, 81), "Test #3f: 'fast_closest_pair' method")


    # 4. check the hierarchical functions
    list_8b = [p8, p2, p6, p4, p5, p3, p7, p1]  # here we have an unsorted list
    suite.run_test(pro.hierarchical_clustering(list_8b, 3)[1].horiz_center(), 0.0, "Test #4a: 'hierarchical_clustering' method")
    list_290 = load_data_table(DATA_290_URL)
    suite.run_test(pro.hierarchical_clustering(list_290, 200)[1].total_population(), 776733, "Test #4b: 'hierarchical_clustering' method")

    p1 = cl.Cluster(set(['1']), -70, 0, 5, 0.5); p2 = cl.Cluster(set(['2']), -50, 0, 1, 0.5); p3 = cl.Cluster(set(['3']), 0, 0, 4, 0.5); p4 = cl.Cluster(set(['4']), 50, 0, 1, 0.5); p5 = cl.Cluster(set(['5']), 70, 0, 3, 0.5)
    list_8c = [p1, p2, p3, p4, p5]  # here we have an unsorted list again, we had to reinitialize it after it was merged above
    suite.run_test(pro.kmeans_clustering(list_8c, 4, 2)[1].horiz_center(), 0.0, "Test #4c: 'kmeans_clustering' method")
    list_896 = load_data_table(DATA_896_URL)
    suite.run_test(pro.kmeans_clustering(list_896, 4, 2)[1].total_population(), 103155706, "Test #4d: 'kmeans_clustering' method")


    # 5. report number of tests and failures
    suite.report_results()


run_suite(alg_cluster)
