import torch
from torch.utils.data.dataloader import DataLoader
from data import PrepASV15Dataset, PrepASV19Dataset
import models
import torch.nn.functional as F
import matplotlib.pyplot as plt
import sys
import numpy as np

def asv_cal_accuracies(protocol, path_data, net, device, data_type='time_frame', dataset=19):
    net = net.to(device)
    net.eval()
    with torch.no_grad():
        softmax_acc = 0
        num_files = 0
        probs = torch.empty(0, 3).to(device) 
        #print("  probs = ", probs)

        if dataset == 15:
            test_set = PrepASV15Dataset(protocol, path_data, data_type=data_type)
        else:
            test_set = PrepASV19Dataset(protocol, path_data, data_type=data_type)
        #print("  test_set = ", test_set)

        #test_loader = DataLoader(test_set, batch_size=64, shuffle=False, num_workers=4)
        test_loader = DataLoader(test_set, batch_size=32, shuffle=False, num_workers=1)
        #print("  test_loader = ", test_loader)

        ii = 0
        for test_batch in test_loader:
            '''
            print("-----------------------------------------------------")
            print("  ii = ", ii)
            print("  test_batch = ", test_batch)
            print("  type(test_batch) = ", type(test_batch))
            '''

            # load batch and infer
            test_sample, test_label, sub_class = test_batch
            '''
            print("    test_sample = ", test_sample)
            print("    test_sample.shape = ", test_sample.shape)
            print("    test_label = ", test_label)
            print("    test_label.shape = ", test_label.shape)
            print("    sub_class = ", sub_class)
            '''
            # # sub_class level test, comment if unwanted
            # # train & dev 0~6; eval 7~19
            # # selected_index = torch.nonzero(torch.logical_xor(sub_class == 10, sub_class == 0))[:, 0]
            # selected_index = torch.nonzero(sub_class.ne(10))[:, 0]
            # if len(selected_index) == 0:
            #     continue
            # test_sample = test_sample[selected_index, :, :]
            # test_label = test_label[selected_index]

            num_files += len(test_label)
            test_sample = test_sample.to(device)
            test_label = test_label.to(device)

            #print("    num_files = ", num_files)
            #print("    test_sample = \n", test_sample)
            #print("    test_label = ", test_label)

            infer = net(test_sample)
            #print("  infer = \n", infer)
            # obtain output probabilities
            t1 = F.softmax(infer, dim=1)
            #print("  t1 = \n", t1)
            t2 = test_label.unsqueeze(-1)
            #print("  t2 = \n", t2)
            row = torch.cat((t1, t2), dim=1)
            #print("  row = \n", row)
            probs = torch.cat((probs, row), dim=0)
            #print("  probs = \n", probs)

            # calculate example level accuracy
            infer = infer.argmax(dim=1)
            #print("  infer = \n", infer)
            batch_acc = infer.eq(test_label).sum().item()
            #print("  batch_acc = ", batch_acc)
            softmax_acc += batch_acc
            ii += 1
        softmax_acc = softmax_acc / num_files

        
    #print("  probs = \n", probs)
    prob_only = probs[:,:2]
    #print("  prob_only = \n", prob_only)
    prob_only_np = prob_only.cpu().numpy()
    #print("  prob_only_np = \n", prob_only_np)
   
    max_prob_np = np.max(prob_only_np, axis=1)
    #print("  max_prob_np = \n", max_prob_np)
    
    class_label = probs[:,2].cpu().numpy()
    #print("  class_label = \n", class_label)
    
    pro_file_list = open(protocol, "r").readlines() 
    #print("  pro_file_list = \n", pro_file_list)
    
    fname = "systhetic_speech_test_result.csv"
    fout = open(fname, "w")
    fout.write("audio_file_name,class_label,probability\n")
    for (ii,ln) in enumerate(pro_file_list):
        flac_prefix = ln.split()[1] 
        flac_name = flac_prefix + '.flac'
        if int(class_label[ii]) == 0: the_label = 'bonafide'
        elif int(class_label[ii]) == 1: the_label = 'spoof'
        #the_label = str(int(class_label[ii]))
        the_prob = max_prob_np[ii]
        '''
        print("  flac_name = ", flac_name)
        print("  the_label = ", the_label)
        print("  the_prob = ", the_prob)
        '''
        fout.write(flac_name + ',' + the_label + ',' + str(the_prob) + '\n')
    fout.close()
    print("  $$$ out file", fname)

    return softmax_acc, probs.to('cpu')


def cal_roc_eer(probs, show_plot=True):
    """
    probs: tensor, number of samples * 3, containing softmax probabilities
    row wise: [genuine prob, fake prob, label]
    TP: True Fake
    FP: False Fake
    """
    all_labels = probs[:, 2]
    zero_index = torch.nonzero((all_labels == 0)).squeeze(-1)
    one_index = torch.nonzero(all_labels).squeeze(-1)
    zero_probs = probs[zero_index, 0]
    one_probs = probs[one_index, 0]

    threshold_index = torch.linspace(-0.1, 1.01, 10000)
    tpr = torch.zeros(len(threshold_index),)
    fpr = torch.zeros(len(threshold_index),)
    cnt = 0
    for i in threshold_index:
        tpr[cnt] = one_probs.le(i).sum().item()/len(one_probs)
        fpr[cnt] = zero_probs.le(i).sum().item()/len(zero_probs)
        cnt += 1

    sum_rate = tpr + fpr
    distance_to_one = torch.abs(sum_rate - 1)
    eer_index = distance_to_one.argmin(dim=0).item()
    out_eer = 0.5*(fpr[eer_index] + 1 - tpr[eer_index]).numpy()

    if show_plot:
        print('EER: {:.4f}%.'.format(out_eer * 100))
        plt.figure(1)
        plt.plot(torch.linspace(-0.2, 1.2, 1000), torch.histc(zero_probs, bins=1000, min=-0.2, max=1.2) / len(zero_probs))
        plt.plot(torch.linspace(-0.2, 1.2, 1000), torch.histc(one_probs, bins=1000, min=-0.2, max=1.2) / len(one_probs))
        plt.xlabel("Probability of 'Genuine'")
        plt.ylabel('Per Class Ratio')
        plt.legend(['Real', 'Fake'])
        plt.grid()

        plt.figure(3)
        plt.scatter(fpr, tpr)
        plt.xlabel('False Positive (Fake) Rate')
        plt.ylabel('True Positive (Fake) Rate')
        plt.grid()
        plt.show()

    return out_eer


if __name__ == '__main__':

    if (len(sys.argv) != 4):
        print("\n")
        print("    Usage: " + sys.argv[0] + " model_file(.pth)  protocol_file  data_dir ")
        print("\n")
        sys.exit(0)

    #protocol_file_path = '/opt/data_ASVspoof2019/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.dev.trl.txt'
    #data_path = '/opt/data_ASVspoof2019/LA/data/dev_6/'
   
    model_file = sys.argv[1]
    protocol_file_path = sys.argv[2]
    data_path = sys.argv[3]


    test_device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    #test_device = torch.device('cuda:3' if torch.cuda.is_available() else 'cpu')
    #test_device = torch.device('cpu')
    
    print("\n")
    print("  model_file = ", model_file)
    print("  protocol_file_path = ", protocol_file_path)
    print("  data_path = ", data_path)
    print("  test_device = ", test_device)
    print("\n")

    Net = models.SSDNet1D()
    #print("  Net = ", Net)
    num_total_learnable_params = sum(i.numel() for i in Net.parameters() if i.requires_grad)
    #print('Number of learnable params: {}.'.format(num_total_learnable_params))

    check_point = torch.load(model_file)
    #print("  check_point = ", check_point)
   
    check_point_model_state_dict = check_point['model_state_dict']
    #print("  check_point_model_state_dict = \n", check_point_model_state_dict)
    
    #Net.load_state_dict(check_point['model_state_dict'])
    Net.load_state_dict(check_point_model_state_dict)
    #print("  Net = ", Net) 
    accuracy, probabilities = asv_cal_accuracies(protocol_file_path, data_path, Net, test_device, data_type='time_frame', dataset=19)
    print("  accuracy = ", accuracy * 100)

    #eer = cal_roc_eer(probabilities)
