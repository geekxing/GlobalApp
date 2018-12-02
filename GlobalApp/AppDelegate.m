//
//  AppDelegate.m
//  GlobalApp
//
//  Created by 赖霄冰 on 2018/12/1.
//  Copyright © 2018 赖霄冰. All rights reserved.
//

#import "AppDelegate.h"
#import "ViewController.h"

@interface AppDelegate ()

@end

@implementation AppDelegate


- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    // Override point for customization after application launch.

    _window = [[UIWindow alloc] initWithFrame:[UIScreen mainScreen].bounds];
    ViewController *rootVC = [[ViewController alloc] init];
    UINavigationController *rootNav = [[UINavigationController alloc] initWithRootViewController:rootVC];
    _window.rootViewController = rootNav;
    [_window makeKeyAndVisible];

    return YES;
}

@end
