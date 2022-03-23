package jp.end0tknr.springvue.controller;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class DemoRestControllerTest {

	@Autowired
	private MockMvc mockMvc;

	@Test
	void testIndex() {
	    assertEquals(1, 1);
	}
	@Test
	void testIndex2() {
	    assertEquals(1, 1);
	}

//	@Test
//	void testIndex3() {
//        try {
//			mockMvc.perform(get("/"))
////			.andDo(print())
//			.andExpect( status().isOk() )
//	        .andExpect( content().string(containsString("Hello")) );
//
//		} catch (Exception e) {
//			e.printStackTrace();
//		}
//	}

}
