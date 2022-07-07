from tagModules.GTM import GTM, TriggerTemple, TimerTrigger, ScrollTrigger

if __name__ == '__main__':
    gtm = GTM()
    timer  = TimerTrigger('TimerTest2', '3000', 'www.carrefour.com.ar', timerType='timerScroll')
    scroll = ScrollTrigger('scrollTest', '50')
