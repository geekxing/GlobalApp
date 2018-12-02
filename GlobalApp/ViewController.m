//
//  ViewController.m
//  GlobalApp
//
//  Created by 赖霄冰 on 2018/12/1.
//  Copyright © 2018 赖霄冰. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@property (nonatomic, strong) UILabel *label;
@property (nonatomic, strong) UIButton *button;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];

    self.automaticallyAdjustsScrollViewInsets = NO;
    self.navigationItem.title = NSLocalizedString(@"多语言", nil);
    self.view.backgroundColor = [UIColor whiteColor];
    [self.view addSubview:self.label];
    [self.view addSubview:self.button];
}

- (UILabel *)label {
    if (!_label) {
        _label = [[UILabel alloc] initWithFrame:CGRectMake(50, 200, 100, 20)];
        _label.text = NSLocalizedString(@"哈哈", nil);
        _label.textAlignment = NSTextAlignmentCenter;
        _label.backgroundColor = [UIColor redColor];
    }
    return _label;
}

- (UIButton *)button {
    if (!_button) {
        _button = [UIButton buttonWithType:UIButtonTypeCustom];
        [_button setTitleColor:[UIColor blackColor] forState:UIControlStateNormal];
        [_button setTitle:NSLocalizedString(@"我的", nil) forState:UIControlStateNormal];
        [_button sizeToFit];
        _button.frame = CGRectMake(100, 100, 50, 50);
        _button.backgroundColor = [UIColor orangeColor];
    }
    return _button;
}

@end
