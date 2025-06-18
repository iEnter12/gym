from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from bookings.models import Booking


class Command(BaseCommand):
    help = '处理预约状态：删除过期未确定的预约和已取消的预约，自动完成到时间的预约'
    
    def handle(self, *args, **options):
        now = timezone.now()
        
        # 1. 删除15分钟内未确定的预约
        expired_bookings = Booking.objects.filter(
            status=0,  # 待确定状态
            create_time__lt=now - timedelta(minutes=15)
        )
        expired_count = expired_bookings.count()
        expired_bookings.delete()
        
        if expired_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'已删除 {expired_count} 个过期未确定的预约')
            )
        
        # 2. 删除已取消的预约（状态为3）
        cancelled_bookings = Booking.objects.filter(status=3)  # 已取消状态
        cancelled_count = cancelled_bookings.count()
        cancelled_bookings.delete()
        
        if cancelled_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'已删除 {cancelled_count} 个已取消的预约')
            )
        
        # 3. 自动完成已过结束时间的预约
        today = now.date()
        current_time = now.time()
        
        # 查找今天已过结束时间且状态为已确定的预约
        auto_complete_bookings = Booking.objects.filter(
            status=1,  # 已确定
            booking_date__lt=today
        ).union(
            Booking.objects.filter(
                status=1,  # 已确定
                booking_date=today,
                end_time__lt=current_time
            )
        )
        
        auto_complete_count = 0
        for booking in auto_complete_bookings:
            booking.status = 2  # 已完成
            booking.save()
            auto_complete_count += 1
        
        if auto_complete_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'已自动完成 {auto_complete_count} 个到时间的预约')
            )
        
        if expired_count == 0 and auto_complete_count == 0:
            self.stdout.write(
                self.style.SUCCESS('没有需要处理的预约')
            )