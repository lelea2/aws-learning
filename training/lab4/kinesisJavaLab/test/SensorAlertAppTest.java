
// Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import static org.junit.Assert.*;
import org.junit.Test;

import java.util.concurrent.TimeUnit;

public class SensorAlertAppTest {
	@Test
	public void testMain() throws Exception {
		SensorAlertApplication.main(new String[0]);
		long endTime = System.currentTimeMillis() + TimeUnit.SECONDS.toMillis(10);
		
		while (System.currentTimeMillis() < endTime && 
		        SensorAlertApplication.getSensorHighTemperatureAlert() == null) {
			Thread.sleep(2000);
		}
		assertNotNull(SensorAlertApplication.getSensorHighTemperatureAlert());

		System.out.printf("SensorAlertAppTest Passed! Received high temperature alert for %s. SensorAlertAppTest Passed! Received high temperature alert for %s!!!", SensorAlertApplication.getSensorHighTemperatureAlert());
	}
}
